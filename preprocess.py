import re

def preprocess(text: str) -> str:
    if not text:                              # handle None or empty string
        return ""
    text = text.lower()                       # step 1: lowercase
    text = re.sub(r'[^a-z0-9 ]', '', text)   # step 2: remove punctuation & non-ASCII
    text = re.sub(r'\s+', ' ', text).strip() # step 3: normalize whitespace
    return text