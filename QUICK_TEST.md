# Quick Test - Removing Config Items

## Before Making Changes

Your current config.json has:
- Types: DRONE, GCS, Radio, BOITE_RADIO, CAMERA, VENTILATEUR, OTHER
- Fields for DRONE: IP, Mesh, SD_Card
- Fields for GCS: IP, Switch
- States: OK, NOK, UNDEFINED, NEEDFIX

## Safe Changes You Can Now Make

### ✅ Remove a field (e.g., "Mesh" from DRONE)
```json
{ "name": "DRONE", "fields": ["IP", "SD_Card"] }
```
**Result**: Existing drones with "Mesh" data won't break. The field just won't show/edit.

### ✅ Remove an entire type (e.g., "VENTILATEUR")
Remove this line from types array:
```json
{ "name": "VENTILATEUR", "fields": [] }
```
**Result**: Existing VENTILATEUR resources will be converted to the first available type.

### ✅ Remove a state (e.g., "NEEDFIX")
```json
"states": ["OK", "NOK", "UNDEFINED"]
```
**Result**: Resources with NEEDFIX status will be converted to UNDEFINED (default).

### ✅ Remove all fields from a type
```json
{ "name": "CAMERA", "fields": [] }
```
**Result**: CAMERA resources will have no editable fields (just title/description).

## What Happens

1. **On App Startup**: Database is automatically scanned and cleaned
2. **When Viewing**: Invalid data is filtered and defaults are applied
3. **When Editing**: Only current fields are shown and saved
4. **No Crashes**: The app continues to work normally

## Try It Now

1. Edit your `config.json` file
2. Remove some fields, types, or states
3. Run: `python main.py`
4. Visit: http://localhost:5000
5. Everything should still work! 🎉
