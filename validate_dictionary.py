import re
import json
from collections import Counter

def validate_dictionary(filepath):
    """Validate the Kannada dictionary for uniqueness and quality."""
    
    print("🔍 Validating Kannada Dictionary")
    print("=" * 60)
    
    # Load words
    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    total_words = len(words)
    print(f"📊 Total words in file: {total_words:,}")
    
    # Check for duplicates
    word_counts = Counter(words)
    duplicates = {word: count for word, count in word_counts.items() if count > 1}
    
    if duplicates:
        print(f"❌ Found {len(duplicates):,} duplicate words:")
        for word, count in list(duplicates.items())[:10]:
            print(f"   '{word}' appears {count} times")
    else:
        print("✅ No duplicates found - all words are unique!")
    
    # Check for empty or whitespace words
    empty_words = [w for w in words if not w or w.isspace()]
    if empty_words:
        print(f"❌ Found {len(empty_words)} empty/whitespace words")
    else:
        print("✅ No empty words found")
    
    # Check for non-Kannada characters
    non_kannada = []
    for word in words:
        if not re.match(r'^[\u0C80-\u0CFF]+$', word):
            non_kannada.append(word)
    
    if non_kannada:
        print(f"⚠️  Found {len(non_kannada):,} words with non-Kannada characters:")
        for word in non_kannada[:10]:
            print(f"   '{word}'")
    else:
        print("✅ All words are in Kannada script")
    
    # Check word length distribution
    print("\n📊 Word length distribution:")
    lengths = Counter()
    for word in words:
        lengths[len(word)] += 1
    
    for length in sorted(lengths.keys())[:15]:
        print(f"   {length:2d} characters: {lengths[length]:,} words")
    print("   ...")
    
    # Check for anomalous patterns
    print("\n🔍 Checking for anomalies:")
    
    # Words that might be too short (single character)
    short_words = [w for w in words if len(w) == 1]
    if short_words:
        print(f"   ⚠️  Found {len(short_words)} single-character words")
        if len(short_words) <= 10:
            print(f"      {short_words}")
    else:
        print("   ✅ No single-character words")
    
    # Words that might be too long (suspicious)
    long_words = [w for w in words if len(w) > 15]
    if long_words:
        print(f"   ⚠️  Found {len(long_words)} words longer than 15 characters")
        if len(long_words) <= 5:
            print(f"      {long_words}")
    else:
        print("   ✅ No suspiciously long words")
    
    # Check for words with repeated patterns
    repeating = []
    for word in words:
        if re.search(r'(.)\1{3,}', word):  # 4+ repeating characters
            repeating.append(word)
    
    if repeating and len(repeating) <= 10:
        print(f"   ⚠️  Found words with repeated characters:")
        for word in repeating[:5]:
            print(f"      '{word}'")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    print(f"   Total words:        {total_words:,}")
    print(f"   Unique:             {'✅ Yes' if not duplicates else '❌ No'}")
    print(f"   Kannada script:     {'✅ All' if not non_kannada else f'⚠️  {len(non_kannada)} issues'}")
    print(f"   Empty words:        {'✅ None' if not empty_words else '❌ Found'}")
    print("=" * 60)
    
    # Save clean version if needed
    if duplicates or non_kannada:
        print("\n💾 Creating cleaned version...")
        clean_words = [w for w in words if re.match(r'^[\u0C80-\u0CFF]+$', w)]
        clean_words = list(set(clean_words))  # Remove duplicates
        
        with open("kannada_master_dictionary_clean.txt", 'w', encoding='utf-8') as f:
            for word in sorted(clean_words):
                f.write(word + '\n')
        
        print(f"   ✅ Cleaned dictionary saved: kannada_master_dictionary_clean.txt")
        print(f"      Clean words: {len(clean_words):,} (removed {len(words) - len(clean_words):,})")
    
    return {
        'total': total_words,
        'unique': not bool(duplicates),
        'kannada_only': not bool(non_kannada)
    }

if __name__ == "__main__":
    validate_dictionary("kannada_master_dictionary.txt")
