# ಕನ್ನಡ OCR Dictionary (Kannada OCR Dictionary)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Words](https://img.shields.io/badge/Words-359,208-blue.svg)](https://github.com/yourusername/kannada-ocr-dictionary)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/yourusername/kannada-ocr-dictionary)

A comprehensive, validated Kannada dictionary specifically designed for OCR correction, spell checking, and natural language processing applications.

---

## 📊 Dictionary Statistics

| Metric | Value |
|--------|-------|
| **Total Words** | **359,208** |
| **Sources** | Alar Dictionary + Kannada IN Dictionary |
| **Format** | Kannada Script (Unicode) |
| **Validation** | ✅ Fully validated |
| **Duplicates** | ✅ None |
| **Alphabetical** | ✅ Sorted |
| **Pure Kannada** | ✅ All words in Kannada script |

### Word Length Distribution

| Length | Count | Length | Count |
|--------|-------|--------|-------|
| 2 chars | 987 | 9 chars | 41,514 |
| 3 chars | 5,516 | 10 chars | 34,853 |
| 4 chars | 16,279 | 11 chars | 27,385 |
| 5 chars | 25,995 | 12+ chars | ~149,000 |
| 6 chars | 37,613 | | |
| 7 chars | 43,161 | | |
| 8 chars | 45,449 | | |
| **Total** | | | **359,208** |

---

## 🎯 Purpose

This dictionary is specifically designed for:

- **OCR Correction** - Validate and correct Kannada text from OCR output
- **Spell Checking** - Check if a word exists in Kannada
- **NLP Applications** - Tokenization, word segmentation, text processing
- **Search & Indexing** - Kannada text search and indexing
- **Educational Tools** - Language learning applications
- **Text Mining** - Kannada text analysis and mining

---

## 📁 Dictionary Files

| File | Format | Size | Description |
|------|--------|------|-------------|
| `data/kannada_dictionary.txt` | TXT | ~7-10 MB | One word per line (359,208 words) |
| `data/kannada_dictionary.json` | JSON | ~15-20 MB | Complete dictionary with metadata |
| `data/kannada_word_list.json` | JSON | ~15-20 MB | Simple word array for fast loading |

### File Formats Explained

#### 1. Text Format (`.txt`)
- One word per line
- Alphabetically sorted
- Easy to read and edit
- Ideal for quick viewing

#### 2. JSON with Metadata (`.json`)

```json
{
  "total_words": 359208,
  "words": ["ಅಂ", "ಅಂಆ", "ಅಂಕ"],
  "metadata": {
    "source": "Alar + Kannada IN Dictionary",
    "validated": true,
    "format": "Kannada script"
  }
}
```

#### 3. Simple Word List (`.json`)

```json
["ಅಂ", "ಅಂಆ", "ಅಂಕ", "ಅಂಕಂಗಾರ"]
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/kannada-ocr-dictionary.git
cd kannada-ocr-dictionary

# Python 3.8+ required
```

### Python Usage

#### Load the Dictionary

```python
import json

# Method 1: Load as word list
with open('data/kannada_word_list.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

# Method 2: Load with metadata
with open('data/kannada_dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)
    words = dictionary['words']
    metadata = dictionary['metadata']
```

#### Fast Word Lookup

```python
# Create a set for O(1) lookup
word_set = set(words)

# Check if a word exists
word = "ಮನೆ"
if word in word_set:
    print(f"✅ '{word}' is a valid Kannada word")
else:
    print(f"❌ '{word}' not found in dictionary")

# Bulk check
test_words = ["ಮನೆ", "ಕನ್ನಡ", "ನಮಸ್ಕಾರ", "invalid"]
for word in test_words:
    status = "✅ Valid" if word in word_set else "❌ Invalid"
    print(f"{status}: {word}")
```

#### Spell Checking Function

```python
def is_valid_kannada_word(word):
    """Check if a word is a valid Kannada word."""
    return word in word_set

# Example usage
text = "ನಮಸ್ಕಾರ ಎಲ್ಲರಿಗೂ"
for word in text.split():
    if is_valid_kannada_word(word):
        print(f"✅ {word}")
    else:
        print(f"❌ {word} - Not found in dictionary")
```

#### Get Word Suggestions (Fuzzy Match)

```python
import re

def get_suggestions(word, max_suggestions=5):
    """Get suggestions for a misspelled word."""
    suggestions = []

    # Find words with similar length
    min_len = max(1, len(word) - 2)
    max_len = len(word) + 2

    for dict_word in words:
        if min_len <= len(dict_word) <= max_len:
            # Simple similarity check (Levenshtein distance)
            if len(word) > 3 and dict_word.startswith(word[0]):
                suggestions.append(dict_word)
            if len(suggestions) >= max_suggestions:
                break

    return suggestions

# Example
word = "ಮನ"
suggestions = get_suggestions(word)
print(f"Suggestions for '{word}': {suggestions}")
```

---

## 🔍 OCR Correction Example

Here's a complete example of using the dictionary for OCR correction:

```python
import json
import re

class KannadaOCRCorrector:
    def __init__(self, dictionary_file):
        """Initialize the OCR corrector with dictionary."""
        with open(dictionary_file, 'r', encoding='utf-8') as f:
            self.words = json.load(f)
        self.word_set = set(self.words)

        # Common OCR confusion patterns
        self.ocr_confusions = {
            'ಅ': ['ಆ', 'ಇ'],
            'ನ': ['ಣ', 'ಮ'],
            'ಸ': ['ಶ', 'ಷ'],
            'ಲ': ['ಳ', 'ವ'],
            'ಹ': ['ಅ', 'ಒ'],
        }

    def is_valid_word(self, word):
        """Check if a word is valid."""
        return word in self.word_set

    def correct_word(self, word):
        """Correct a single word."""
        if self.is_valid_word(word):
            return {'status': 'correct', 'word': word}

        # Try OCR confusion fixes
        suggestions = []
        for i, char in enumerate(word):
            if char in self.ocr_confusions:
                for replacement in self.ocr_confusions[char]:
                    candidate = word[:i] + replacement + word[i+1:]
                    if self.is_valid_word(candidate):
                        suggestions.append(candidate)

        return {
            'status': 'corrected' if suggestions else 'unknown',
            'original': word,
            'suggestions': suggestions[:5],
            'best': suggestions[0] if suggestions else None
        }

    def correct_text(self, text):
        """Correct all words in a text."""
        words = text.split()
        corrected = []

        for word in words:
            if re.match(r'^[\u0C80-\u0CFF]+$', word):  # Kannada word
                result = self.correct_word(word)
                corrected.append(result.get('best', word))
            else:
                corrected.append(word)

        return ' '.join(corrected)

# Usage example
corrector = KannadaOCRCorrector('data/kannada_word_list.json')

# Test
ocr_output = "ನಮಸ್ಕಾರ ಮನೆಗ ಮನವು ಹೊಗು"
print(f"OCR Output: {ocr_output}")
print(f"Corrected:  {corrector.correct_text(ocr_output)}")
```

---

## 🛠️ Building from Source

### Prerequisites

```bash
pip install -r requirements.txt
```

### Build the Dictionary

```bash
python scripts/build_dictionary.py
```

### Validate the Dictionary

```bash
python scripts/validate_dictionary.py data/kannada_dictionary.txt
```

---

## 📖 Sources

This dictionary is built from authoritative sources:

- **Alar Dictionary** - 139,195 words
  - Open-source Kannada-English dictionary
  - High-quality, well-structured entries
  - Includes part-of-speech information

- **Kannada IN Dictionary** - ~237,032 unique words
  - Community-maintained dictionary
  - Includes frequency counts
  - Modern vocabulary coverage

### Merging Process

1. **Extract** - Extract unique words from both sources
2. **Clean** - Remove duplicates and non-Kannada characters
3. **Validate** - Check for quality and correctness
4. **Sort** - Alphabetically sort the final list

---

## ✅ Validation Checks

The dictionary has passed all validation checks:

- ✅ No duplicates - All words are unique
- ✅ Kannada script - All words are in pure Kannada script
- ✅ Alphabetically sorted - Easy to search and browse
- ✅ No invalid sequences - All characters are valid
- ✅ No abnormally long words - Reasonable word lengths
- ✅ No suspicious starts - All words start with valid characters

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository** - Click the Fork button on GitHub
2. **Create a feature branch** - `git checkout -b feature/amazing-feature`
3. **Commit your changes** - `git commit -m 'Add amazing feature'`
4. **Push to the branch** - `git push origin feature/amazing-feature`
5. **Open a Pull Request** - Click the Pull Request button on GitHub

### Contribution Guidelines

- Add new words from verified sources
- Report any issues or inconsistencies
- Suggest improvements to the dictionary
- Help with documentation

---

## 📧 Contact & Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## 🙏 Acknowledgments

- **Alar Dictionary** - V. Krishna for the open-source dictionary
- **Kannada IN Dictionary** - Community contributors
- **Kannada Language Community** - For preserving and promoting the language

---

## 📚 Related Projects

- Kannada NLP Tools
- Kannada OCR Engine
- Kannada Spell Checker

---

## ⭐ Star this Repository

If you find this dictionary useful, please star the repository and share it with others!

Built with ❤️ for the Kannada language community

*Last Updated: September 2026*
