import requests
import re

print("📚 Downloading IndoWordNet Kannada word list...")

# Method 1: Try to download from Hugging Face directly
try:
    # Use the raw data URL from Hugging Face
    url = "https://huggingface.co/datasets/cfilt/iwn_wordlists/resolve/main/kannada/wordlist.txt"
    
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        words = set()
        for line in response.text.splitlines():
            word = line.strip()
            # Keep only Kannada script words
            if re.match(r'^[\u0C80-\u0CFF]+$', word) and len(word) > 1:
                words.add(word)
        
        print(f"✅ Downloaded {len(words):,} unique Kannada words")
        
        # Save to file
        with open("indowordnet_kannada_words.txt", "w", encoding="utf-8") as f:
            for word in sorted(words):
                f.write(word + "\n")
        print(f"💾 Saved to indowordnet_kannada_words.txt")
    else:
        print(f"❌ Download failed with status: {response.status_code}")
        print("   Trying alternative source...")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Trying alternative source...")
