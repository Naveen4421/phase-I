from datasets import load_dataset

print("📚 Loading Kannada word list from IndoWordNet...")

# Load the Kannada word list
words = load_dataset("cfilt/iwn_wordlists", "kannada")

# Get the word list from the training split
word_list = words["train"]["word"]

# View the first few words
print(f"\n✅ Loaded {len(word_list)} words from IndoWordNet")
print("\n📝 First 10 words:")
print(word_list[:10])

# Save the word list to a file
with open("indowordnet_kannada_words.txt", "w", encoding="utf-8") as f:
    for word in word_list:
        f.write(word + "\n")

print(f"\n💾 Saved all words to indowordnet_kannada_words.txt")
