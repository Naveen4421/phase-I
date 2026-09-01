import re
import json
from pathlib import Path

def load_kannada_in_file(filepath, name):
    """Load words from Kannada IN Dictionary - preserving Kannada words even with mixed characters."""
    words = set()
    
    if not Path(filepath).exists():
        print(f"   ⚠️  {name} not found at {filepath}")
        return words
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"   📖 {name}: Processing {len(lines):,} lines")
        
        # Process each line
        valid_count = 0
        filtered_count = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Split by whitespace - format: "frequency word"
            parts = line.split()
            if len(parts) >= 2:
                # First part is frequency (number), rest is the word
                freq = parts[0]
                word = ' '.join(parts[1:])  # Join in case word has spaces
            elif len(parts) == 1:
                # Only one part - it's the word
                word = parts[0]
            else:
                continue
            
            # Clean the word
            word = word.strip()
            
            # Keep words that contain Kannada characters (even if they have other chars)
            if word and len(word) > 1:
                # Check if word has at least one Kannada character
                if re.search(r'[\u0C80-\u0CFF]', word):
                    # Remove non-Kannada characters but keep Kannada
                    # Keep only Kannada script characters
                    cleaned_word = ''.join(re.findall(r'[\u0C80-\u0CFF]', word))
                    
                    # Only add if we have a valid Kannada word
                    if cleaned_word and len(cleaned_word) > 1:
                        words.add(cleaned_word)
                        valid_count += 1
                    else:
                        filtered_count += 1
        
        print(f"   ✅ {name}: {len(words):,} words extracted")
        print(f"      (Valid: {valid_count:,}, Filtered: {filtered_count:,})")
        
    except Exception as e:
        print(f"   ❌ Error loading {name}: {e}")
    
    return words

def load_alar_words():
    """Load words from Alar dictionary."""
    words = set()
    try:
        with open("kannada_dictionary_phase1.txt", 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word and re.match(r'^[\u0C80-\u0CFF]+$', word) and len(word) > 1:
                    words.add(word)
        print(f"   ✅ Alar Dictionary: {len(words):,} words")
    except Exception as e:
        print(f"   ❌ Error loading Alar: {e}")
    return words

def load_hunspell_if_available():
    """Load Hunspell dictionary if available."""
    words = set()
    try:
        if Path("kn_IN.dic").exists():
            with open("kn_IN.dic", 'r', encoding='utf-8') as f:
                f.readline()  # Skip count
                for line in f:
                    word = line.strip()
                    if '/' in word:
                        word = word.split('/')[0]
                    if word and re.match(r'^[\u0C80-\u0CFF]+$', word) and len(word) > 1:
                        words.add(word)
            print(f"   ✅ Hunspell Dictionary: {len(words):,} words")
    except Exception:
        pass
    return words

print("📚 Creating Complete Kannada Master Dictionary (Fixed)")
print("=" * 60)

# Load all sources
print("\n📖 Loading all sources...")

alar_words = load_alar_words()
kannada_in_main = load_kannada_in_file("kannada_in_dictionary_words.txt", "Kannada IN Dictionary (Main)")
kannada_in_processed = load_kannada_in_file("kannada_in_dictionary_words_processed.txt", "Kannada IN Dictionary (Processed)")
hunspell_words = load_hunspell_if_available()

# Merge all words
all_words = set()
all_words.update(alar_words)
all_words.update(kannada_in_main)
all_words.update(kannada_in_processed)
all_words.update(hunspell_words)

print("\n" + "=" * 60)
print(f"📊 Total unique Kannada words: {len(all_words):,}")
print("\n📊 Source breakdown:")
print(f"   Alar Dictionary:               {len(alar_words):,}")
print(f"   Kannada IN Dictionary (Main):  {len(kannada_in_main):,}")
print(f"   Kannada IN Dictionary (Proc):  {len(kannada_in_processed):,}")
print(f"   Hunspell Dictionary:           {len(hunspell_words):,}")
print(f"   {'─' * 45}")
print(f"   Total unique words:            {len(all_words):,}")

# Save master list
with open("kannada_master_dictionary.txt", 'w', encoding='utf-8') as f:
    for word in sorted(all_words):
        f.write(word + '\n')
print(f"\n💾 Saved: kannada_master_dictionary.txt ({len(all_words):,} words)")

# Save JSON
with open("kannada_master_dictionary.json", 'w', encoding='utf-8') as f:
    json.dump(sorted(list(all_words)), f, ensure_ascii=False, indent=2)
print(f"💾 Saved: kannada_master_dictionary.json")

# Show sample
print("\n📝 Sample words from merged dictionary:")
sample = sorted(all_words)[:20]
for i, word in enumerate(sample, 1):
    print(f"   {i:2d}. {word}")

print("\n✅ Complete! Master dictionary created.")
