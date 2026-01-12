# Test the Default Images Feature

## Setup Complete! ✅

Default images have been created:
- `static/images/default_DRONE.png` 
- `static/images/default_GCS.png`

## How to Test

### Test 1: Create a DRONE without uploading an image

1. Start the app: `python main.py`
2. Click "Create" button
3. Fill in:
   - **Title**: Test Drone 1
   - **Type**: DRONE
   - **Status**: OK
4. **Don't upload an image** - leave the image field empty
5. Click Submit

**Expected Result**: The new drone should display with the default DRONE image! 🚁

### Test 2: Create a GCS without uploading an image

1. Click "Create" again
2. Fill in:
   - **Title**: Test GCS 1
   - **Type**: GCS
   - **Status**: OK
3. **Don't upload an image**
4. Click Submit

**Expected Result**: The new GCS should display with the default GCS image! 🎮

### Test 3: Create a CAMERA (no default image)

1. Click "Create"
2. Fill in:
   - **Title**: Test Camera 1
   - **Type**: CAMERA
   - **Status**: OK
3. **Don't upload an image**
4. Click Submit

**Expected Result**: The camera shows "No image" placeholder (no default exists for CAMERA yet)

### Test 4: Upload overrides default

1. Click "Create"
2. Fill in:
   - **Title**: Custom Drone
   - **Type**: DRONE
3. **Upload your own image**
4. Click Submit

**Expected Result**: Your uploaded image is used instead of the default

## Add More Default Images

To add defaults for other types:

```powershell
# Example: Create default for Radio type
Copy-Item "path\to\your\radio.png" "static\images\default_Radio.png"

# Example: Create default for CAMERA
Copy-Item "path\to\your\camera.png" "static\images\default_CAMERA.png"
```

Or just add any PNG file named `default_TYPE.png` to `static/images/`!

## Verify Files

Check what default images exist:
```powershell
Get-ChildItem "static\images\default_*.png"
```
