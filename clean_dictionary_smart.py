import re
import json

def clean_dictionary_smart(input_file, output_file):
    """Smart clean the dictionary - remove only real issues."""
    
    print("🧹 SMART CLEANING KANNADA DICTIONARY")
    print("=" * 60)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    print(f"📊 Original words: {len(words):,}")
    
    clean_words = set()
    removed = {
        'invalid_start': 0,      # Words starting with ಂ or ಃ
        'too_long': 0,           # Words > 25 chars
        'invalid_sequence': 0,   # Invalid vowel sequences
        'non_kannada': 0,        # Non-Kannada chars (should be 0)
    }
    
    # Valid Kannada characters
    valid_kannada = re.compile(r'^[\u0C80-\u0CFF]+$')
    
    for word in words:
        # 1. Remove words starting with Anusvara or Visarga
        # (These are usually OCR errors or incomplete words)
        if word[0] in ['ಂ', 'ಃ', 'ಀ']:
            removed['invalid_start'] += 1
            continue
        
        # 2. Remove abnormally long words (> 25 chars)
        # These are usually compound words or OCR errors
        if len(word) > 25:
            removed['too_long'] += 1
            continue
        
        # 3. Remove words with invalid sequences
        # Check for 3+ consecutive vowels (invalid in Kannada)
        if re.search(r'[ಅಆಇಈಉಊಋಎಏಐಒಓಔ]{3,}', word):
            removed['invalid_sequence'] += 1
            continue
        
        # 4. Remove non-Kannada characters (should be none)
        if not valid_kannada.match(word):
            removed['non_kannada'] += 1
            continue
        
        clean_words.add(word)
    
    print(f"📊 Clean words: {len(clean_words):,}")
    print(f"\n🗑️  Removed:")
    for reason, count in removed.items():
        if count > 0:
            print(f"   {reason}: {count:,}")
    
    # Save cleaned dictionary
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(clean_words):
            f.write(word + '\n')
    
    print(f"\n💾 Cleaned dictionary saved: {output_file}")
    
    # Show sample of removed words
    print("\n📝 Sample removed words:")
    removed_words = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for word in f:
            word = word.strip()
            if word[0] in ['ಂ', 'ಃ', 'ಀ']:
                removed_words.append(word)
            if len(removed_words) >= 10:
                break
    if removed_words:
        print("   Starting with Anusvara/Visarga:")
        for w in removed_words[:5]:
            print(f"      {w}")
    
    # Check long words
    long_words = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for word in f:
            word = word.strip()
            if len(word) > 25:
                long_words.append(word)
            if len(long_words) >= 10:
                break
    if long_words:
        print("\n   Long words (>25 chars):")
        for w in long_words[:5]:
            print(f"      {w[:30]}...")
    
    return clean_words

if __name__ == "__main__":
    clean_dictionary_smart("kannada_master_dictionary.txt", "kannada_dictionary_clean.txt")
