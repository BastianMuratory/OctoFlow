# Resource Management (Flask)

A small Flask app to manage resources with image uploads, per-type attributes, and a simple SQLite backend.

---

## ✅ Quick overview

- Built with **Python + Flask** and **SQLite**.
- Uploads are saved to `static/uploads/` and resource metadata is stored in `resources.db`.
- Per-"Type" attributes are stored as JSON in the `attributes` column.

---

## 🔧 Requirements

- Python 3.10+ (3.11/3.12 recommended)
- pip

Optional dev tools:
- `pyflakes` or `flake8` for linting
- `black` for formatting

---

## ⚙️ Installation (Windows / cross-platform)

1. Clone the repo or open the project folder.
2. (Recommended) Create and activate a virtual environment:

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install Flask
# (optional) pip install pyflakes flake8 black
```

Tip: To capture installed packages for future use run `pip freeze > requirements.txt`.

---

## ▶️ Run the app

Start the app locally:

```bash
python main.py
```

Then open: http://127.0.0.1:5000

Notes:
- The app will create `static/uploads/` automatically if missing.
- Database `resources.db` is created/initialized when the app starts (see `init_db()` in `main.py`).

---

## 🗂️ Project structure (important files)

- `main.py` – Flask app, routes for Create/Edit/Delete, DB helpers, upload handling.
- `enumeration.py` – `Type` and `State` enums used for dropdowns and status.
- `templates/` – Jinja2 templates (`index.html`, `create.html`).
- `static/` – CSS, JS and `uploads/` for images.
- `resources.db` – SQLite DB (created at runtime).

---

## ✏️ Development notes & tips

- Type-specific fields are defined in `config.json` (see `types` ➜ `fields`). Edit `config.json` to add/remove types and their fields — no code change required.
- The app loads Types and States from `config.json` at startup and uses them for dropdowns and field rendering.
- Attributes are filtered server-side so only allowed attributes for the chosen type are saved (prevents stale/invalid fields).
- To reset the DB: stop the server, delete `resources.db`, restart the app (it will recreate the table).
- Image filenames are saved as-is (sanitized with `werkzeug.utils.secure_filename`) and saved under `static/uploads/`. If a filename already exists, it will be overwritten.

---

## 🐞 Troubleshooting

- ModuleNotFoundError: Install Flask inside the active venv: `pip install Flask`.
- Write permission errors when saving uploads: check `static/uploads/` folder permissions.
- Template rendering errors: inspect Flask console output for tracebacks and confirm templates are present in `templates/`.

---

## 🧩 Extending the app

- Add new Type values: update `enumeration.py` and add corresponding allowed fields in `TYPE_FIELDS` (in `main.py`).
- Add server-side validation or richer front-end validation for attributes.
- Add pagination/filtering server-side for large datasets.

---

## 📞 Contact / Next steps

If you want, I can:
- Add a `requirements.txt` and a Windows PowerShell startup script.
- Add unit tests for repository functions and Flask endpoints.

---

**Enjoy — GitHub Copilot**
