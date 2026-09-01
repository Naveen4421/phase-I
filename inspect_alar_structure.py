import yaml
import json

print("🔍 Inspecting Alar YAML Structure")
print("=" * 60)

# Load the YAML file
with open("alar_dictionary.yaml", 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

print(f"📊 Total entries: {len(data):,}")
print(f"📊 Type of data: {type(data)}")

# Show first few entries with their complete structure
print("\n📝 First 5 entries (full structure):")
print("-" * 60)

for i, entry in enumerate(data[:5]):
    if isinstance(entry, dict):
        print(f"\nEntry {i+1}:")
        print(json.dumps(entry, ensure_ascii=False, indent=2)[:1000])
        print("-" * 40)

# Look for any field that might contain POS information
print("\n🔍 Searching for POS-related fields...")
print("-" * 60)

pos_fields = set()
sample_entries = []

for entry in data:
    if not isinstance(entry, dict):
        continue
    
    # Collect all field names
    for key in entry.keys():
        pos_fields.add(key)
    
    # Find entries that might have POS info
    if 'type' in entry or 'pos' in entry or 'category' in entry or 'class' in entry:
        sample_entries.append(entry)
        if len(sample_entries) >= 3:
            break

print(f"All field names found: {sorted(pos_fields)}")

if sample_entries:
    print("\n📝 Entries with POS-like fields:")
    for entry in sample_entries:
        print(json.dumps(entry, ensure_ascii=False, indent=2)[:500])
        print("-" * 40)
else:
    print("\n⚠️  No entries found with 'type', 'pos', 'category', or 'class' fields")
    
    # Show a few entries to see what fields exist
    print("\n📝 Sample entries to understand structure:")
    for i, entry in enumerate(data[:3]):
        if isinstance(entry, dict):
            print(f"\nEntry {i+1} fields: {list(entry.keys())}")
            print(f"Entry {i+1} content:")
            for key, value in entry.items():
                if isinstance(value, str) and len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")
            print("-" * 40)

# Check if 'info' field contains POS info
print("\n🔍 Checking 'info' field for POS indicators:")
print("-" * 60)

pos_indicators = ['noun', 'verb', 'adj', 'adv', 'pron', 'conj', 'prep', 'interj']
info_samples = []

for entry in data:
    if isinstance(entry, dict) and 'info' in entry:
        info = entry.get('info', '').lower()
        for indicator in pos_indicators:
            if indicator in info:
                info_samples.append(entry)
                break
    if len(info_samples) >= 5:
        break

if info_samples:
    print("Entries where 'info' contains POS indicators:")
    for entry in info_samples:
        print(f"  Word: {entry.get('entry')}")
        print(f"  Info: {entry.get('info')}")
        print(f"  Type: {entry.get('type', 'No type field')}")
        print()
else:
    print("No POS indicators found in 'info' field")

print("\n" + "=" * 60)
print("✅ Inspection complete!")
