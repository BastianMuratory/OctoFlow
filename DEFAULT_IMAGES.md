# Default Images Feature

## How It Works

When creating or editing a resource without uploading an image, the system automatically checks for a default image based on the resource type.

## Naming Convention

Default images must be named: `default_TYPE.png`

Where `TYPE` matches exactly the type name from your config.json.

## Examples

Based on your current config.json types:

- **DRONE** → `default_DRONE.png`
- **GCS** → `default_GCS.png`
- **Radio** → `default_Radio.png`
- **BOITE_RADIO** → `default_BOITE_RADIO.png`
- **CAMERA** → `default_CAMERA.png`
- **VENTILATEUR** → `default_VENTILATEUR.png`
- **OTHER** → `default_OTHER.png`

## Where to Place Default Images

Put your default images in: `static/images/`

Example structure:
```
static/
  images/
    default_DRONE.png
    default_GCS.png
    default_Radio.png
    default_CAMERA.png
  uploads/
    (user uploaded images go here automatically)
```

## Behavior

1. **Creating a resource:**
   - User uploads an image → Uses uploaded image
   - User doesn't upload → Checks for `default_TYPE.png`
   - No default found → Resource has no image

2. **Editing a resource:**
   - User uploads new image → Uses new image
   - User doesn't upload, has existing → Keeps existing
   - User doesn't upload, no existing → Checks for `default_TYPE.png`
   - No default found → Resource has no image

## Quick Setup

To add default images:

1. Create or find PNG images for your types
2. Rename them following the `default_TYPE.png` convention
3. Copy them to `static/images/` folder
4. Create new resources without uploading images
5. The default images will be used automatically! 🎉

## Notes

- Default images are **read-only** - they stay in `static/images/`
- Uploaded images go to `static/uploads/` 
- You can mix both: some types with defaults, others without
- Case-sensitive: `default_DRONE.png` ≠ `default_drone.png`
