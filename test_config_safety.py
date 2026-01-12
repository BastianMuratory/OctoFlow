"""
Test script to verify the application handles config.json changes gracefully.
This simulates removing fields and types from config.json.
"""
import json
import os
import shutil

# Backup original config
if os.path.exists("config.json"):
    shutil.copy("config.json", "config.json.backup")
    print("✓ Created backup: config.json.backup")

# Test 1: Remove some fields from DRONE type
print("\nTest 1: Removing fields from DRONE type...")
with open("config.json", "r") as f:
    config = json.load(f)

for t in config["types"]:
    if t["name"] == "DRONE":
        original_fields = t["fields"].copy()
        t["fields"] = []  # Remove all fields
        print(f"  Original fields: {original_fields}")
        print(f"  New fields: {t['fields']}")

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
print("  ✓ Config updated")

# Test 2: Remove a type entirely
print("\nTest 2: Removing a type...")
with open("config.json", "r") as f:
    config = json.load(f)

original_types = [t["name"] for t in config["types"]]
config["types"] = [t for t in config["types"] if t["name"] != "VENTILATEUR"]
new_types = [t["name"] for t in config["types"]]
print(f"  Original types: {original_types}")
print(f"  New types: {new_types}")

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
print("  ✓ Config updated")

# Test 3: Remove some states
print("\nTest 3: Removing states...")
with open("config.json", "r") as f:
    config = json.load(f)

original_states = config["states"].copy()
config["states"] = ["OK", "NOK"]  # Keep only 2 states
print(f"  Original states: {original_states}")
print(f"  New states: {config['states']}")

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
print("  ✓ Config updated")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
print("\nNow run your Flask app with: python main.py")
print("The app should:")
print("  1. Start without errors")
print("  2. Show all existing resources with sanitized data")
print("  3. Handle removed fields gracefully")
print("  4. Update database entries to valid values")
print("\nTo restore original config: ")
print("  copy config.json.backup config.json")
