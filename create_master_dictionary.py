import re
import json
from pathlib import Path

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

def load_kannada_in_words(filepath, name):
    """Load words from Kannada IN Dictionary files."""
    words = set()
    try:
        if not Path(filepath).exists():
            print(f"   ⚠️  {name} not found")
            return words
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Handle format: "word" or "word frequency"
                parts = line.split()
                if parts:
                    word = parts[0]  # First part is the word
                    # Keep only Kannada script
                    if re.match(r'^[\u0C80-\u0CFF]+$', word) and len(word) > 1:
                        words.add(word)
        print(f"   ✅ {name}: {len(words):,} words")
    except Exception as e:
        print(f"   ❌ Error loading {name}: {e}")
    return words

def load_hunspell_words():
    """Load words from Hunspell dictionary if available."""
    words = set()
    try:
        if not Path("kn_IN.dic").exists():
            return words
        
        with open("kn_IN.dic", 'r', encoding='utf-8') as f:
            # Skip first line (count)
            first = f.readline()
            for line in f:
                word = line.strip()
                if '/' in word:
                    word = word.split('/')[0]
                if word and re.match(r'^[\u0C80-\u0CFF]+$', word) and len(word) > 1:
                    words.add(word)
        print(f"   ✅ Hunspell Dictionary: {len(words):,} words")
    except Exception as e:
        print(f"   ⚠️  Hunspell not available: {e}")
    return words

print("📚 Creating Complete Kannada Master Dictionary")
print("=" * 60)

# Load all sources
print("\n📖 Loading all sources...")

alar_words = load_alar_words()
kannada_in_main = load_kannada_in_words("kannada_in_dictionary_words.txt", "Kannada IN Dictionary (Main)")
kannada_in_processed = load_kannada_in_words("kannada_in_dictionary_words_processed.txt", "Kannada IN Dictionary (Processed)")
hunspell_words = load_hunspell_words()

# Merge all words
all_words = set()
all_words.update(alar_words)
all_words.update(kannada_in_main)
all_words.update(kannada_in_processed)
all_words.update(hunspell_words)

print("\n" + "=" * 60)
print(f"📊 Total unique Kannada words: {len(all_words):,}")
print("\n📊 Source breakdown:")

# Count contributions
print(f"   Alar Dictionary:               {len(alar_words):,}")
print(f"   Kannada IN Dictionary (Main):  {len(kannada_in_main):,}")
print(f"   Kannada IN Dictionary (Proc):  {len(kannada_in_processed):,}")
print(f"   Hunspell Dictionary:           {len(hunspell_words):,}")
print(f"   {'─' * 45}")
print(f"   Total unique words:            {len(all_words):,}")

# Save to files
print("\n💾 Saving dictionary files...")

# Text file (one word per line)
with open("kannada_master_dictionary.txt", 'w', encoding='utf-8') as f:
    for word in sorted(all_words):
        f.write(word + '\n')
print(f"   ✅ Master text: kannada_master_dictionary.txt ({len(all_words):,} words)")

# JSON file
with open("kannada_master_dictionary.json", 'w', encoding='utf-8') as f:
    json.dump(sorted(list(all_words)), f, ensure_ascii=False, indent=2)
print(f"   ✅ Master JSON: kannada_master_dictionary.json")

# Frequency-based breakdown
print("\n📊 Word length distribution:")
lengths = {}
for word in all_words:
    l = len(word)
    lengths[l] = lengths.get(l, 0) + 1

for l in sorted(lengths.keys())[:15]:
    print(f"   {l} characters: {lengths[l]:,} words")
print("   ...")

print("\n📊 First 20 words:")
for i, word in enumerate(sorted(all_words)[:20]):
    print(f"   {i+1:2d}. {word}")

print("\n✅ Complete! Master dictionary created.")
