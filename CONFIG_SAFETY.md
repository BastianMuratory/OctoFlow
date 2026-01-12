# Config Safety Implementation

## Overview
The application now handles `config.json` modifications gracefully without breaking the database or causing errors.

## Changes Made

### 1. Enhanced Config Loading ([main.py](main.py))
- **Defensive defaults**: Always ensures `types` and `states` arrays exist with at least one entry
- **Field validation**: Ensures each type has a `fields` array (empty if not specified)
- **Fallback behavior**: Returns sensible defaults if config file is corrupted or missing

### 2. Data Sanitization Functions ([main.py](main.py))
Added three new utility functions:

- `sanitize_attributes(attrs, category)`: Removes attributes that no longer exist in config
- `sanitize_status(status)`: Ensures status is valid, returns default if not
- `sanitize_category(category)`: Ensures category exists, returns first available type if not

### 3. Automatic Database Cleanup ([main.py](main.py))
New `cleanup_orphaned_data()` function that:
- Runs automatically on app startup
- Fixes invalid categories in existing resources
- Fixes invalid status values
- Removes attributes with fields that no longer exist in config
- Doesn't crash the app if cleanup encounters errors

### 4. Route Protection
All routes now sanitize data:

**Index route (`/`)**:
- Sanitizes category, status, and attributes for each resource before display
- Handles missing or invalid data gracefully

**Create route (`/create`)**:
- Sanitizes category before saving
- Only saves attributes that exist in current config

**Edit route (`/edit/<id>`)**:
- Sanitizes category and status on submit
- Filters out removed fields from attributes
- Displays only valid fields when loading existing resource

### 5. Template Safety ([templates/create.html](templates/create.html))
- Added checks for empty `types` and `states` arrays
- Provides fallback options if config is empty
- Uses safe defaults with Jinja's `|default()` filter

## How It Works

### When You Remove a Type
**Example**: Remove "VENTILATEUR" from config

1. Existing resources with `category="VENTILATEUR"` are automatically updated to the first available type
2. The UI only shows currently available types in dropdowns
3. No database errors occur

### When You Remove Fields
**Example**: Remove "Mesh" field from DRONE type

1. Existing DRONE resources keep the "Mesh" attribute in the database
2. The attribute is filtered out when displaying or editing
3. When saving edits, removed fields are cleaned from the database
4. No errors occur when accessing resources

### When You Remove States
**Example**: Remove "NEEDFIX" state

1. Resources with `status="NEEDFIX"` are updated to the default state
2. Only current states appear in dropdowns
3. Status icons for removed states simply don't display

## Testing

Run the test script to verify safety:
```powershell
python test_config_safety.py
```

This will:
1. Backup your config
2. Simulate removing fields, types, and states
3. Provide instructions for manual testing

Then start the app:
```powershell
python main.py
```

The app should work normally despite the config changes.

## Safety Guarantees

✅ **No crashes** when config items are removed
✅ **No data loss** - database preserves all data
✅ **Automatic cleanup** - orphaned data is sanitized on startup
✅ **Graceful degradation** - removed fields simply don't display
✅ **Safe defaults** - always falls back to valid values

## Important Notes

- The database is **not immediately modified** when you change config
- Data is sanitized **on-the-fly** when loading resources
- Permanent cleanup happens when you **edit and save** a resource
- The `cleanup_orphaned_data()` function runs on every app startup to fix inconsistencies
- Original data is preserved in the database until explicitly updated

## Rollback

If you need to restore removed config items:
1. Add them back to `config.json`
2. Restart the app
3. Old data with those fields/types will automatically reappear
