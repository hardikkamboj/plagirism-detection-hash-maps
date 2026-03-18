"""
Generate a synthetic plagiarism corpus from Project Gutenberg books.

Strategy:
  1. Download a few public-domain books
  2. Split each into fixed-size chunks (~150 words)
  3. Label all chunks as "original"
  4. Create plagiarized docs by copying random chunks verbatim into new entries
  5. Write corpus.csv

Run:  python generate_corpus.py
"""

import csv
import random
import re
import urllib.request

# --- config ---
CHUNK_WORDS    = 150    # words per chunk
PLAGIARISM_RATE = 0.3   # 30% of docs will be plagiarized copies
SEED           = 42
OUTPUT         = 'corpus.csv'

BOOKS = [
    ('pride_and_prejudice', 'https://www.gutenberg.org/files/1342/1342-0.txt'),
    ('alice_in_wonderland', 'https://www.gutenberg.org/files/11/11-0.txt'),
    ('moby_dick',           'https://www.gutenberg.org/files/2701/2701-0.txt'),
]

random.seed(SEED)


def fetch_book(url: str) -> str:
    print(f"  Downloading {url} ...")
    with urllib.request.urlopen(url, timeout=30) as r:
        raw = r.read().decode('utf-8-sig', errors='ignore')

    # strip Gutenberg header/footer
    start = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG', raw)
    end   = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG',   raw)
    if start and end:
        raw = raw[start.end():end.start()]

    return re.sub(r'\s+', ' ', raw).strip()


def chunk_text(text: str, chunk_words: int) -> list[str]:
    words  = text.split()
    chunks = []
    for i in range(0, len(words) - chunk_words + 1, chunk_words):
        chunks.append(' '.join(words[i:i + chunk_words]))
    return chunks


# --- build corpus ---
rows = []
all_chunks = []   # (doc_id, text) — pool to sample plagiarised copies from

print("Fetching books...")
for book_name, url in BOOKS:
    try:
        text   = fetch_book(url)
        chunks = chunk_text(text, CHUNK_WORDS)
        print(f"  {book_name}: {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            doc_id = f"{book_name}_{i:04d}"
            rows.append({
                'file_name': doc_id,
                'text':      chunk,
                'category':  'original',
                'source':    book_name,
            })
            all_chunks.append((doc_id, chunk))
    except Exception as e:
        print(f"  WARNING: could not fetch {book_name}: {e}")

if not all_chunks:
    raise SystemExit("No books downloaded — check your internet connection.")

# --- add plagiarised copies ---
n_plagiarised = int(len(all_chunks) * PLAGIARISM_RATE)
sampled       = random.sample(all_chunks, n_plagiarised)

for idx, (src_id, src_text) in enumerate(sampled):
    rows.append({
        'file_name': f"plagiarised_{idx:04d}",
        'text':      src_text,          # verbatim copy
        'category':  'plagiarized',
        'source':    src_id,            # points back to the original
    })

# --- shuffle and write ---
random.shuffle(rows)

with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['file_name', 'text', 'category', 'source'])
    writer.writeheader()
    writer.writerows(rows)

total_orig = sum(1 for r in rows if r['category'] == 'original')
total_plag = sum(1 for r in rows if r['category'] == 'plagiarized')
print(f"\nDone: {len(rows)} documents written to {OUTPUT}")
print(f"  original:   {total_orig}")
print(f"  plagiarized:{total_plag}")
