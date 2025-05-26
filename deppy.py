import os
import ast
import importlib.util
import importlib.metadata
import sysconfig
import sys

PROJECT_ROOT = "."

used_modules = set()

# --- Step 1: Collect top-level imports ---
for root, _, files in os.walk(PROJECT_ROOT):
    for file in files:
        if file.endswith(".py") and not file.startswith("._"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for name in node.names:
                                used_modules.add(name.name.split('.')[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                used_modules.add(node.module.split('.')[0])
            except (SyntaxError, UnicodeDecodeError):
                print(f"Skipped malformed file: {file_path}")

# --- Step 2: Filters ---
stdlib_path = sysconfig.get_path('stdlib')

def is_stdlib(mod_name):
    try:
        spec = importlib.util.find_spec(mod_name)
        return spec and spec.origin and spec.origin.startswith(stdlib_path)
    except Exception:
        return False

def is_local_module(mod_name):
    for root, _, files in os.walk(PROJECT_ROOT):
        if f"{mod_name}.py" in files:
            return True
    return False

def is_in_site_packages(mod_name):
    try:
        spec = importlib.util.find_spec(mod_name)
        if spec and spec.origin:
            return "site-packages" in spec.origin or "dist-packages" in spec.origin
        return False
    except Exception:
        return False

# --- Step 3: Build package list ---
project_packages = {}

for mod in sorted(used_modules):
    if is_stdlib(mod) or is_local_module(mod):
        continue
    if not is_in_site_packages(mod):
        continue
    try:
        version = importlib.metadata.version(mod)
        project_packages[mod] = version
    except importlib.metadata.PackageNotFoundError:
        continue  # if no version info, skip

# --- Step 4: Output ---
print("\nDetected third-party packages:")
for name, version in sorted(project_packages.items()):
    print(f"{name}=={version}")
