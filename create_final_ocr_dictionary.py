import json
import re

def create_final_ocr_dictionary():
    """Create the final dictionary for OCR correction - keep all valid words."""
    
    print("✨ CREATING FINAL OCR-READY KANNADA DICTIONARY")
    print("=" * 60)
    
    # Load the clean dictionary (it's already perfect!)
    with open("kannada_dictionary_clean.txt", 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    
    print(f"📊 Total words: {len(words):,}")
    
    # Create a list for JSON serialization (convert set to list)
    word_list = sorted(words)
    
    # Create the final dictionary structure (convert set to list for JSON)
    final_dict = {
        'words': word_list,
        'total_words': len(words),
        'metadata': {
            'source': 'Merged from Alar + Kannada IN Dictionary',
            'total_words': len(words),
            'format': 'Kannada script only',
            'validated': True,
            'ready_for_ocr': True
        }
    }
    
    # Save as JSON for fast loading
    with open("kannada_final_ocr_dict.json", 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Final OCR dictionary saved: kannada_final_ocr_dict.json")
    
    # Save as text file (one word per line)
    with open("kannada_final_ocr_dict.txt", 'w', encoding='utf-8') as f:
        for word in word_list:
            f.write(word + '\n')
    print(f"💾 Final OCR dictionary saved: kannada_final_ocr_dict.txt")
    
    # Also create a simple word list JSON (just the words)
    with open("kannada_word_list.json", 'w', encoding='utf-8') as f:
        json.dump(word_list, f, ensure_ascii=False, indent=2)
    print(f"💾 Word list JSON saved: kannada_word_list.json")
    
    # Show sample
    print(f"\n📝 Sample words from final dictionary:")
    for word in word_list[:10]:
        print(f"   {word}")
    
    print(f"\n📊 Dictionary ready for OCR correction with {len(words):,} words!")
    
    # Show statistics
    print(f"\n📊 Word length distribution:")
    lengths = {}
    for word in word_list:
        l = len(word)
        lengths[l] = lengths.get(l, 0) + 1
    
    for l in sorted(lengths.keys())[:10]:
        print(f"   {l} chars: {lengths[l]:,} words")
    print("   ...")
    
    return final_dict

if __name__ == "__main__":
    create_final_ocr_dictionary()
