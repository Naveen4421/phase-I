import yaml
import re
import json
from collections import defaultdict

def load_master_words():
    """Load the master word list."""
    with open("kannada_master_dictionary.txt", 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

def categorize_words_from_alar(yaml_file, master_words):
    """Categorize words using Alar dictionary metadata."""
    
    print("📚 Loading Alar YAML metadata...")
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print(f"   Alar has {len(data):,} entries")
    
    # Initialize categories
    categories = {
        'noun': set(),
        'verb': set(),
        'pronoun': set(),
        'adjective': set(),
        'adverb': set(),
        'postposition': set(),
        'conjunction': set(),
        'interjection': set(),
        'other': set()
    }
    
    # Keywords for each POS (in Kannada and English)
    pos_keywords = {
        'noun': ['noun', 'n.', 'n', 'ನಾಮಪದ', 'ಸಂಜ್ಞಾ', 'namapada', 'ಸಂಜ್ಞೆ'],
        'verb': ['verb', 'v.', 'v', 'ಕ್ರಿಯಾಪದ', 'kriyapada', 'ಕ್ರಿಯಾ'],
        'pronoun': ['pronoun', 'pron.', 'pron', 'ಸರ್ವನಾಮ', 'sarvanama'],
        'adjective': ['adj', 'adjective', 'ವಿಶೇಷಣ', 'viseshana', 'ವಿಶೇಷ'],
        'adverb': ['adv', 'adverb', 'ಕ್ರಿಯಾವಿಶೇಷಣ', 'kriyaviseshana'],
        'postposition': ['post', 'postposition', 'ವಿಭಕ್ತಿ', 'vibhakti'],
        'conjunction': ['conj', 'conjunction', 'ಸಮುಚ್ಚಯ', 'samucchaya'],
        'interjection': ['interj', 'interjection', 'ವಿಸ್ಮಯ', 'vismaya']
    }
    
    print("\n📖 Processing Alar entries...")
    
    # Track words that were categorized
    categorized_words = set()
    total_processed = 0
    
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            continue
        
        word = entry.get('entry', '').strip()
        
        # Skip if word not in master dictionary
        if word not in master_words:
            continue
        
        total_processed += 1
        
        # Get POS information from various fields
        pos_info = ''
        if 'type' in entry and entry['type']:
            pos_info += str(entry['type']).lower() + ' '
        if 'info' in entry and entry['info']:
            pos_info += str(entry['info']).lower() + ' '
        if 'head' in entry and entry['head']:
            head = str(entry['head']).lower()
            pos_info += head + ' '
        
        # Check if the word has POS info
        word_categorized = False
        
        for category, keywords in pos_keywords.items():
            if any(keyword in pos_info for keyword in keywords):
                categories[category].add(word)
                categorized_words.add(word)
                word_categorized = True
                break
        
        # If no category matched, put in 'other'
        if not word_categorized:
            categories['other'].add(word)
            categorized_words.add(word)
        
        if (i + 1) % 10000 == 0:
            print(f"   Processed {i+1:,} entries... Categorized {len(categorized_words):,} words")
    
    print(f"\n✅ Processed {total_processed:,} words from master list")
    print(f"   Categorized {len(categorized_words):,} words")
    
    # Words from master list not in Alar
    uncategorized = master_words - categorized_words
    print(f"   Words not in Alar: {len(uncategorized):,}")
    
    return categories, uncategorized

def save_categories(categories, uncategorized):
    """Save each category to a separate file."""
    
    print("\n💾 Saving categorized dictionaries...")
    
    total_words = 0
    for category, words in categories.items():
        if words:
            filename = f"kannada_{category}s.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for word in sorted(words):
                    f.write(word + '\n')
            print(f"   ✅ {category.capitalize():12s}: {len(words):,} words → {filename}")
            total_words += len(words)
    
    # Save uncategorized words
    if uncategorized:
        with open("kannada_uncategorized.txt", 'w', encoding='utf-8') as f:
            for word in sorted(uncategorized):
                f.write(word + '\n')
        print(f"   ⚠️  Uncategorized:          {len(uncategorized):,} words → kannada_uncategorized.txt")
        total_words += len(uncategorized)
    
    # Create a master JSON with all categories
    master_dict = {}
    for category, words in categories.items():
        if words:
            master_dict[category] = sorted(list(words))
    master_dict['uncategorized'] = sorted(list(uncategorized))
    
    with open("kannada_dictionary_by_pos.json", 'w', encoding='utf-8') as f:
        json.dump(master_dict, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Master JSON saved: kannada_dictionary_by_pos.json")
    
    return total_words

def main():
    print("=" * 60)
    print("📚 KANNADA DICTIONARY - PARTS OF SPEECH CATEGORIZATION")
    print("=" * 60)
    
    # Load master words
    print("\n📖 Loading master dictionary...")
    master_words = load_master_words()
    print(f"   Master has {len(master_words):,} words")
    
    # Categorize
    categories, uncategorized = categorize_words_from_alar("alar_dictionary.yaml", master_words)
    
    # Save
    total_words = save_categories(categories, uncategorized)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 CATEGORIZATION SUMMARY")
    print("=" * 60)
    for category, words in sorted(categories.items()):
        if words:
            print(f"   {category.capitalize():12s}: {len(words):,} words")
    if uncategorized:
        print(f"   {'Uncategorized':12s}: {len(uncategorized):,} words")
    print(f"   {'─' * 25}")
    print(f"   {'Total':12s}: {total_words:,} words")
    print("=" * 60)
    
    # Show samples
    print("\n📝 Sample words from each category:")
    for category, words in categories.items():
        if words:
            sample = sorted(words)[:5]
            print(f"   {category.capitalize()}: {', '.join(sample)}")
    if uncategorized:
        sample = sorted(uncategorized)[:5]
        print(f"   Uncategorized: {', '.join(sample)}")

if __name__ == "__main__":
    main()
