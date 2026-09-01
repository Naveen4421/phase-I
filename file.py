import yaml
import re
import os
import sys

def load_alar_words(alar_file_path):
    """Extracts unique Kannada entry words from the Alar YAML file."""
    alar_words = set()
    try:
        print("   Opening YAML file...")
        with open(alar_file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        print(f"   YAML loaded. Type: {type(data)}")
        
        # Handle different YAML structures
        if isinstance(data, list):
            print(f"   Processing list with {len(data)} items...")
            for i, entry in enumerate(data):
                if isinstance(entry, dict) and 'entry' in entry:
                    alar_words.add(entry['entry'].strip())
                if i % 10000 == 0:
                    print(f"   Processed {i} items...")
                    
        elif isinstance(data, dict):
            print(f"   Processing dictionary with keys: {list(data.keys())[:5]}")
            # Try different common structures
            if 'entries' in data and isinstance(data['entries'], list):
                for entry in data['entries']:
                    if isinstance(entry, dict) and 'entry' in entry:
                        alar_words.add(entry['entry'].strip())
            else:
                # Try to find entries in the dictionary
                for key, value in data.items():
                    if isinstance(value, dict) and 'entry' in value:
                        alar_words.add(value['entry'].strip())
                    elif key == 'entry' and isinstance(value, str):
                        alar_words.add(value.strip())
                # If still nothing, try to find any string values
                if not alar_words:
                    for key, value in data.items():
                        if isinstance(value, str) and len(value) > 1:
                            # Check if it looks like Kannada
                            if re.match(r'^[\u0C80-\u0CFF]+$', value):
                                alar_words.add(value)
        
        print(f"   Loaded {len(alar_words)} total words.")
        
    except FileNotFoundError:
        print(f"❌ Error: Alar file not found at {alar_file_path}")
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return alar_words

def clean_and_save_words(words, output_file_path):
    """Cleans and saves the word list."""
    print("🧹 Cleaning words...")
    clean_words = set()
    
    for word in words:
        # Remove whitespace
        word = word.strip()
        # Keep only Kannada script
        if not re.match(r'^[\u0C80-\u0CFF]+$', word):
            continue
        # Filter out single characters or very short words
        if len(word) <= 1:
            continue
        clean_words.add(word)
    
    print(f"   Cleaned to {len(clean_words)} words.")
    
    print("💾 Saving words...")
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for word in sorted(list(clean_words)):
                f.write(word + '\n')
        print(f"✅ Successfully saved to {output_file_path}")
        return len(clean_words)
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return 0

def inspect_yaml_structure(file_path):
    """Helper function to inspect YAML structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            data = yaml.safe_load(f)
            print("\n🔍 YAML Structure Inspection:")
            print(f"   Type: {type(data)}")
            if isinstance(data, dict):
                print(f"   Keys ({len(data.keys())}): {list(data.keys())[:10]}")
                if data:
                    sample_key = list(data.keys())[0]
                    sample_value = data[sample_key]
                    print(f"   Sample key '{sample_key}' type: {type(sample_value)}")
                    if isinstance(sample_value, dict):
                        print(f"   Sample value keys: {list(sample_value.keys())[:10]}")
                    elif isinstance(sample_value, str):
                        print(f"   Sample value (first 50 chars): {sample_value[:50]}")
            elif isinstance(data, list):
                print(f"   Length: {len(data)}")
                if data:
                    print(f"   First item type: {type(data[0])}")
                    if isinstance(data[0], dict):
                        print(f"   First item keys: {list(data[0].keys())[:10]}")
                        if 'entry' in data[0]:
                            print(f"   First entry: {data[0]['entry']}")
            print()
    except Exception as e:
        print(f"❌ Error inspecting YAML: {e}")

if __name__ == "__main__":
    ALAR_YAML_PATH = "alar_dictionary.yaml"
    OUTPUT_TXT_PATH = "kannada_dictionary_phase1.txt"
    
    print("🔍 Phase 1: Kannada Dictionary Pipeline (Alar-only)")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(ALAR_YAML_PATH):
        print(f"❌ Error: {ALAR_YAML_PATH} not found!")
        print("   Run: cp data/alar.yml alar_dictionary.yaml")
        exit(1)
    
    # Inspect structure first
    inspect_yaml_structure(ALAR_YAML_PATH)
    
    # Load words
    print("📚 Loading Alar words...")
    alar_words = load_alar_words(ALAR_YAML_PATH)
    
    if len(alar_words) == 0:
        print("❌ Error: No words loaded! The YAML structure might be different.")
        print("   The inspection above shows the structure. Please share it for debugging.")
        exit(1)
    
    # Clean and save
    word_count = clean_and_save_words(alar_words, OUTPUT_TXT_PATH)
    
    print("\n✅ Phase 1 complete!")
    print(f"   Output: {OUTPUT_TXT_PATH}")
    print(f"   Word count: {word_count}")
