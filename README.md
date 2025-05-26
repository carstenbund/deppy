# deppy

**deppy** is a lightweight Python dependency scanner that extracts real imports used in your project and generates a clean `requirements.txt`, without the bloat of `pip freeze`.

Unlike `pip freeze`, which lists **all installed packages**, `deppy` scans your actual `.py` source files, detects `import` statements, filters out:
- standard library modules (e.g., `os`, `time`, `sqlite3`)
- local project files (e.g., `mem_database.py`)
- and only outputs packages installed via `pip` and located in `site-packages`

---

## Features

- Scans all `.py` files in your project recursively
- Extracts top-level imports using Python’s AST (safe, syntax-aware)
- Excludes standard library and local modules
- Detects only 3rd-party dependencies installed in `site-packages`
- Prints versions using `importlib.metadata` (no deprecated APIs)
- Outputs a ready-to-use `requirements.txt`

---

## Example Output

```text
Detected third-party packages:
openai==1.72.0
requests==2.31.0

