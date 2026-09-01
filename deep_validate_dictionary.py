import re
import json
from collections import Counter

def deep_validate_dictionary(filepath):
    """Perform deep validation on the Kannada dictionary."""
    
    print("🔍 DEEP VALIDATION OF KANNADA DICTIONARY")
    print("=" * 60)
    
    # Load words
    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    total = len(words)
    print(f"📊 Total words: {total:,}")
    
    # 1. Check for duplicates
    print("\n1️⃣ CHECKING FOR DUPLICATES")
    print("-" * 40)
    word_counts = Counter(words)
    duplicates = {w: c for w, c in word_counts.items() if c > 1}
    if duplicates:
        print(f"❌ Found {len(duplicates):,} duplicate words!")
        # Show duplicates with count > 2
        for word, count in sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   '{word}' appears {count} times")
    else:
        print("✅ No duplicates found!")
    
    # 2. Check for non-Kannada characters
    print("\n2️⃣ CHECKING FOR NON-KANNADA CHARACTERS")
    print("-" * 40)
    non_kannada = []
    for word in words:
        if not re.match(r'^[\u0C80-\u0CFF]+$', word):
            non_kannada.append(word)
    if non_kannada:
        print(f"❌ Found {len(non_kannada):,} words with non-Kannada characters!")
        for word in non_kannada[:10]:
            print(f"   '{word}'")
    else:
        print("✅ All words are in Kannada script!")
    
    # 3. Check for invalid Kannada character sequences
    print("\n3️⃣ CHECKING FOR INVALID KANNADA SEQUENCES")
    print("-" * 40)
    invalid_sequences = []
    # Kannada valid character ranges
    valid_chars = re.compile(r'^[\u0C80-\u0CFF]+$')
    # Check for isolated vowels without consonants (common in OCR errors)
    for word in words:
        if re.search(r'[ಅಆಇಈಉಊಋಎಏಐಒಓಔ]', word):
            # Check if there's a valid consonant-vowel combination
            if not re.search(r'[\u0C95-\u0CD6][\u0CBE-\u0CCC]', word):
                # Only flag if the vowel is not standalone
                if len(word) > 1:
                    invalid_sequences.append(word)
    
    if invalid_sequences:
        print(f"⚠️  Found {len(invalid_sequences):,} words with potentially invalid sequences")
        print(f"   (First 5: {invalid_sequences[:5]})")
    else:
        print("✅ No invalid sequences found!")
    
    # 4. Check for very short words (1 character)
    print("\n4️⃣ CHECKING FOR VERY SHORT WORDS")
    print("-" * 40)
    short_words = [w for w in words if len(w) == 1]
    if short_words:
        print(f"⚠️  Found {len(short_words)} single-character words:")
        for word in short_words[:10]:
            print(f"   '{word}'")
        # Check if they're valid Kannada characters
        valid_single = [w for w in short_words if re.match(r'^[\u0C80-\u0CFF]$', w)]
        print(f"   Valid single characters: {len(valid_single)}")
        invalid_single = [w for w in short_words if not re.match(r'^[\u0C80-\u0CFF]$', w)]
        if invalid_single:
            print(f"   ⚠️  Invalid single characters: {invalid_single}")
    else:
        print("✅ No single-character words!")
    
    # 5. Check for abnormally long words
    print("\n5️⃣ CHECKING FOR ABNORMALLY LONG WORDS")
    print("-" * 40)
    long_words = [w for w in words if len(w) > 25]
    if long_words:
        print(f"⚠️  Found {len(long_words):,} words longer than 25 characters")
        print(f"   First 5: {long_words[:5]}")
    else:
        print("✅ No abnormally long words!")
    
    # 6. Check for words starting with weird characters
    print("\n6️⃣ CHECKING FOR WORDS WITH SUSPICIOUS STARTS")
    print("-" * 40)
    suspicious_starts = []
    for word in words:
        if word[0] in ['ಂ', 'ಃ', 'ಀ']:
            suspicious_starts.append(word)
    if suspicious_starts:
        print(f"⚠️  Found {len(suspicious_starts):,} words starting with Anusvara or Visarga")
        print(f"   First 10: {suspicious_starts[:10]}")
        print("\n   These might be OCR errors or compound words.")
    else:
        print("✅ No words with suspicious starts!")
    
    # 7. Check for correct alphabetical ordering
    print("\n7️⃣ CHECKING ALPHABETICAL ORDER")
    print("-" * 40)
    sorted_words = sorted(words)
    if words == sorted_words:
        print("✅ Dictionary is properly alphabetically sorted!")
    else:
        print("⚠️  Dictionary is NOT fully alphabetically sorted")
        # Find first mismatch
        for i, (a, b) in enumerate(zip(words, sorted_words)):
            if a != b:
                print(f"   First mismatch at position {i}:")
                print(f"   Current: {a}")
                print(f"   Should be: {b}")
                break
    
    # 8. Check for common OCR error patterns
    print("\n8️⃣ CHECKING FOR COMMON OCR ERROR PATTERNS")
    print("-" * 40)
    ocr_errors = []
    confusion_pairs = {
        'ಅ': ['ಆ', 'ಇ'],
        'ನ': ['ಣ', 'ಮ'],
        'ಸ': ['ಶ', 'ಷ'],
        'ಲ': ['ಳ', 'ವ'],
        'ಹ': ['ಅ', 'ಒ'],
    }
    for word in words:
        for char, errors in confusion_pairs.items():
            if char in word:
                for error in errors:
                    if error in word:
                        ocr_errors.append((word, char, error))
    if ocr_errors:
        print(f"⚠️  Found {len(ocr_errors):,} words with potential OCR error patterns")
        print(f"   First 5:")
        for word, expected, actual in ocr_errors[:5]:
            print(f"   '{word}' (contains '{actual}' instead of '{expected}')")
    else:
        print("✅ No common OCR error patterns found!")
    
    # 9. Check word length distribution
    print("\n9️⃣ WORD LENGTH DISTRIBUTION")
    print("-" * 40)
    lengths = {}
    for word in words:
        l = len(word)
        lengths[l] = lengths.get(l, 0) + 1
    
    # Show main lengths
    for l in sorted(lengths.keys())[:10]:
        print(f"   {l:2d} chars: {lengths[l]:,} words")
    print("   ...")
    
    # 10. Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    issues = []
    if duplicates:
        issues.append(f"⚠️  {len(duplicates)} duplicate words")
    if non_kannada:
        issues.append(f"⚠️  {len(non_kannada)} non-Kannada words")
    if invalid_sequences:
        issues.append(f"⚠️  {len(invalid_sequences)} invalid sequences")
    if short_words:
        issues.append(f"⚠️  {len(short_words)} single-character words")
    if long_words:
        issues.append(f"⚠️  {len(long_words)} abnormally long words")
    if suspicious_starts:
        issues.append(f"⚠️  {len(suspicious_starts)} suspicious starts")
    if ocr_errors:
        issues.append(f"⚠️  {len(ocr_errors)} potential OCR errors")
    
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 RECOMMENDATION: Clean the dictionary before using for OCR correction.")
    else:
        print("✅ DICTIONARY IS PERFECT! No issues found!")
    
    # Save detailed report
    report = {
        'total_words': total,
        'duplicates': len(duplicates),
        'non_kannada': len(non_kannada),
        'invalid_sequences': len(invalid_sequences),
        'short_words': len(short_words),
        'long_words': len(long_words),
        'suspicious_starts': len(suspicious_starts),
        'ocr_errors': len(ocr_errors),
        'perfect': not any([
            duplicates, non_kannada, invalid_sequences, 
            short_words, long_words, suspicious_starts, ocr_errors
        ])
    }
    
    with open("dictionary_validation_report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("\n📄 Detailed report saved: dictionary_validation_report.json")
    
    return report

if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "kannada_master_dictionary.txt"
    deep_validate_dictionary(filepath)
