from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import json
from werkzeug.utils import secure_filename

# load a config.json to drive available types, their per-type fields, and states
def load_config(path="config.json"):
    defaults = {
        "types": [
            {"name": "DRONE", "fields": ["rotors", "battery"]},
            {"name": "GCS", "fields": ["firmware"]},
            {"name": "OTHER", "fields": []}
        ],
        "states": ["OK", "NOK", "UNDEFINED", "NEEDFIX"]
    }
    
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Ensure types and states exist and have at least one entry
                if not config.get('types') or len(config.get('types', [])) == 0:
                    config['types'] = defaults['types']
                if not config.get('states') or len(config.get('states', [])) == 0:
                    config['states'] = defaults['states']
                # Ensure each type has a name and fields list
                for t in config.get('types', []):
                    if 'fields' not in t:
                        t['fields'] = []
                return config
        except Exception:
            pass
    # fallback defaults
    return defaults

CONFIG = load_config()
# default status used when no status is provided
DEFAULT_STATE = CONFIG.get('states', ['UNDEFINED'])[0] if CONFIG.get('states') else 'UNDEFINED'
# map of type name -> allowed fields (used server-side to validate attributes)
TYPE_FIELDS = {t.get('name', 'UNKNOWN'): t.get('fields', []) for t in CONFIG.get('types', []) if t.get('name')}

app = Flask(__name__)
DB = "resources.db"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_column(conn, table, column, coltype):
    """Ensure a column exists on a table by checking PRAGMA table_info and adding it if missing."""
    cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")


def cleanup_orphaned_data():
    """Clean up database entries that reference removed config items."""
    conn = get_db()
    try:
        # Get all resources
        rows = conn.execute("SELECT id, category, status, attributes FROM resource").fetchall()
        
        valid_categories = set(TYPE_FIELDS.keys())
        valid_states = set(CONFIG.get('states', [DEFAULT_STATE]))
        
        for row in rows:
            resource_id = row['id']
            category = row['category']
            status = row['status']
            attrs_raw = row['attributes']
            
            needs_update = False
            new_category = category
            new_status = status
            new_attrs = None
            
            # Fix invalid category
            if category not in valid_categories:
                new_category = sanitize_category(category)
                needs_update = True
            
            # Fix invalid status
            if status not in valid_states:
                new_status = sanitize_status(status)
                needs_update = True
            
            # Fix attributes with removed fields
            if attrs_raw:
                try:
                    attrs = json.loads(attrs_raw)
                    sanitized_attrs = sanitize_attributes(attrs, new_category)
                    if attrs != sanitized_attrs:
                        new_attrs = json.dumps(sanitized_attrs) if sanitized_attrs else None
                        needs_update = True
                except Exception:
                    new_attrs = None
                    needs_update = True
            
            # Update if necessary
            if needs_update:
                conn.execute(
                    "UPDATE resource SET category = ?, status = ?, attributes = ? WHERE id = ?",
                    (new_category, new_status, new_attrs, resource_id)
                )
        
        conn.commit()
    except Exception as e:
        # If cleanup fails, log but don't crash the app
        print(f"Warning: Database cleanup encountered an error: {e}")
    finally:
        conn.close()

def init_db():
    conn = get_db()

    # create the table if it's missing (includes all desired columns so new DBs are correct)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS resource (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            category TEXT,
            image_filename TEXT,
            to_display INTEGER,
            status TEXT,
            attributes TEXT
        )
    """)

    # ensure columns exist on older DBs (safe to call multiple times)
    try:
        ensure_column(conn, "resource", "image_filename", "TEXT")
        ensure_column(conn, "resource", "attributes", "TEXT")
        ensure_column(conn, "resource", "status", "TEXT")
        # previous versions allowed hiding resources; migrate existing rows to be visible
        try:
            conn.execute("UPDATE resource SET to_display = 1 WHERE to_display IS NULL OR to_display = 0")
        except Exception:
            # if the column doesn't exist yet or update fails, ignore
            pass
    except Exception:
        # if migration fails for some reason, don't crash the app here
        pass

    conn.commit()
    conn.close()
    
    # Clean up any orphaned data after initialization
    cleanup_orphaned_data()


def sanitize_attributes(attrs, category):
    """Remove attributes that are no longer defined in config for the given category."""
    if not attrs or not isinstance(attrs, dict):
        return {}
    allowed_fields = TYPE_FIELDS.get(category, [])
    return {k: v for k, v in attrs.items() if k in allowed_fields}

def sanitize_status(status):
    """Ensure status is valid, return default if not."""
    valid_states = CONFIG.get('states', [DEFAULT_STATE])
    if status and status in valid_states:
        return status
    return DEFAULT_STATE

def sanitize_category(category):
    """Ensure category exists in config, return first type if not."""
    if category and category in TYPE_FIELDS:
        return category
    # Return first available type or 'OTHER' as fallback
    types = CONFIG.get('types', [])
    return types[0].get('name', 'OTHER') if types else 'OTHER'

@app.route("/")
def index():
    conn = get_db()
    # fetch all resources, we'll control visibility client-side
    rows = conn.execute(
        "SELECT * FROM resource"
    ).fetchall()
    resources = []
    for r in rows:
        d = dict(r)
        # Parse attributes
        if d.get("attributes"):
            try:
                d["attributes"] = json.loads(d["attributes"])
            except Exception:
                d["attributes"] = {}
        else:
            d["attributes"] = {}
        
        # Sanitize category to ensure it exists in current config
        d["category"] = sanitize_category(d.get("category"))
        
        # Sanitize attributes based on current config
        d["attributes"] = sanitize_attributes(d["attributes"], d["category"])
        
        # Sanitize status to ensure it's valid
        d["status"] = sanitize_status(d.get("status"))
        
        # ensure to_display exists and is 0/1
        # visibility flag removed: always visible
        d["to_display"] = 1
        resources.append(d)
    conn.close()
    return render_template("index.html", resources=resources, types=CONFIG.get('types', []), states=CONFIG.get('states', []), status_val=DEFAULT_STATE)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"].replace('\r\n','\n').replace('<br>','\n').replace('<br/>','\n').replace('<br />','\n')
        category = request.form["category"]
        file = request.files.get("image")
        filename = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # no visibility toggles any more — always set resources to visible
        to_display = 1

        # sanitize category before proceeding
        category = sanitize_category(category)
        
        # collect dynamic attribute fields only for the selected category
        attrs = {}
        allowed = TYPE_FIELDS.get(category, [])
        for k in allowed:
            v = request.form.get(k)
            if v is not None and v != "":
                attrs[k] = v
        attrs_json = json.dumps(attrs) if attrs else None

        conn = get_db()
        conn.execute(
            """
            INSERT INTO resource (title, description, category, image_filename, to_display, status, attributes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (title, description, category, filename, to_display, request.form.get('status', DEFAULT_STATE), attrs_json),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    # pass available types and states to template for dropdowns
    return render_template("create.html", types=CONFIG.get('types', []), states=CONFIG.get('states', []), status_val=DEFAULT_STATE)

@app.route("/edit/<int:resource_id>", methods=["GET", "POST"])
def edit(resource_id):
    conn = get_db()
    if request.method == "POST":
        # get current resource to preserve image when no new file uploaded
        current = conn.execute("SELECT * FROM resource WHERE id = ?", (resource_id,)).fetchone()

        file = request.files.get("image")
        filename = current["image_filename"] if current else None

        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        # sanitize category before proceeding
        submitted_category = sanitize_category(request.form.get('category'))
        submitted_status = sanitize_status(request.form.get('status', DEFAULT_STATE))
        
        # merge attributes: keep only allowed fields for the new category
        allowed = TYPE_FIELDS.get(submitted_category, [])
        existing_attrs = {}
        if current:
            try:
                current_raw = current["attributes"]
            except Exception:
                current_raw = None
            if current_raw:
                try:
                    existing_attrs = json.loads(current_raw)
                except Exception:
                    existing_attrs = {}
        # filter to allowed keys only (this removes fields from other types)
        filtered = {k: v for k, v in existing_attrs.items() if k in allowed}
        # update with submitted allowed fields
        for k in allowed:
            val = request.form.get(k)
            if val is None or val == "":
                filtered.pop(k, None)
            else:
                filtered[k] = val
        attrs_json = json.dumps(filtered) if filtered else None

        # normalize description textarea input similarly to create
        desc_clean = request.form["description"].replace('\r\n','\n').replace('<br>','\n').replace('<br/>','\n').replace('<br />','\n')
        conn.execute("""
            UPDATE resource
            SET title = ?, description = ?, category = ?, image_filename = ?, to_display = ?, status = ?, attributes = ?
            WHERE id = ?
        """, (
            request.form["title"],
            desc_clean,
            submitted_category,
            filename,
            1,  # always visible
            submitted_status,
            attrs_json,
            resource_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    resource = conn.execute(
        "SELECT * FROM resource WHERE id = ?", (resource_id,)
    ).fetchone()

    attrs = {}
    status_val = DEFAULT_STATE
    if resource:
        # Get category and sanitize it
        resource_category = sanitize_category(resource.get('category') if hasattr(resource, 'get') else resource['category'])
        
        try:
            resource_raw = resource["attributes"]
        except Exception:
            resource_raw = None
        if resource_raw:
            try:
                attrs = json.loads(resource_raw)
                # Sanitize attributes based on current config
                attrs = sanitize_attributes(attrs, resource_category)
            except Exception:
                attrs = {}
        try:
            status_val = sanitize_status(resource['status'] if resource['status'] else None)
        except Exception:
            status_val = DEFAULT_STATE

    conn.close()

    return render_template("create.html", resource=resource, types=CONFIG.get('types', []), attrs=attrs, states=CONFIG.get('states', []), status_val=status_val)


@app.route('/delete/<int:resource_id>', methods=['POST'])
def delete(resource_id):
    conn = get_db()
    try:
        row = conn.execute('SELECT id, image_filename FROM resource WHERE id = ?', (resource_id,)).fetchone()
        if row:
            # remove image file if present
            try:
                filename = row['image_filename']
            except Exception:
                filename = None
            if filename:
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception:
                    pass
            conn.execute('DELETE FROM resource WHERE id = ?', (resource_id,))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)