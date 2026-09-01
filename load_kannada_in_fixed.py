import re
import json
from pathlib import Path

def load_kannada_in_file(filepath, name):
    """Load words from Kannada IN Dictionary with proper format handling."""
    words = set()
    
    if not Path(filepath).exists():
        print(f"   ⚠️  {name} not found at {filepath}")
        return words
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'utf-16', 'latin-1', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    
                # Check if we got any valid content
                if lines and any(line.strip() for line in lines[:10]):
                    print(f"   ✅ Successfully read with {encoding} encoding")
                    break
            except:
                continue
        else:
            print(f"   ❌ Could not read {name} with any encoding")
            return words
        
        # Process each line
        for i, line in enumerate(lines[:10]):
            print(f"   Line {i+1}: {repr(line[:50])}")
        
        # Now actually extract words
        word_count = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try different formats:
            # Format 1: "word"
            # Format 2: "word frequency"
            # Format 3: "word\tfrequency"
            # Format 4: "word\tlemma\tfrequency"
            
            parts = line.split()
            if parts:
                word = parts[0]  # First part is the word
                
                # Clean the word
                word = word.strip()
                
                # Remove any special characters or punctuation
                word = re.sub(r'[^\u0C80-\u0CFF]', '', word)
                
                # Keep only Kannada words
                if word and len(word) > 1 and re.match(r'^[\u0C80-\u0CFF]+$', word):
                    words.add(word)
                    word_count += 1
        
        print(f"   ✅ {name}: {len(words):,} words extracted (processed {word_count:,} lines)")
        
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

print("🔍 Loading Kannada IN Dictionary with detailed debugging...")
print("=" * 60)

# Test loading the Kannada IN files
kannada_in_main = load_kannada_in_file("kannada_in_dictionary_words.txt", "Kannada IN Dictionary (Main)")
kannada_in_processed = load_kannada_in_file("kannada_in_dictionary_words_processed.txt", "Kannada IN Dictionary (Processed)")

# Also load Alar for comparison
print("\n📖 Loading Alar...")
alar_words = load_alar_words()

# Merge
all_words = set()
all_words.update(alar_words)
all_words.update(kannada_in_main)
all_words.update(kannada_in_processed)

print("\n" + "=" * 60)
print(f"📊 Total unique Kannada words: {len(all_words):,}")
print(f"   Alar: {len(alar_words):,}")
print(f"   Kannada IN Main: {len(kannada_in_main):,}")
print(f"   Kannada IN Processed: {len(kannada_in_processed):,}")

# Save merged
with open("kannada_master_dictionary_updated.txt", 'w', encoding='utf-8') as f:
    for word in sorted(all_words):
        f.write(word + '\n')

print(f"\n💾 Saved to kannada_master_dictionary_updated.txt")
