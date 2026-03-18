"""
Convert train_snli.txt → corpus.csv

Input format (tab-separated):
  sentence1 \t sentence2 \t label   (1=plagiarized, 0=not)

Output corpus.csv columns:
  file_name, text, category, source

Strategy:
  - sentence1 rows → "original" documents (the source texts)
  - sentence2 rows → "plagiarized" or "original" based on label
"""

import csv
import sys

INPUT  = 'train_snli.txt'
OUTPUT = 'corpus.csv'
MAX_ROWS = None   # set to e.g. 5000 to limit size for testing

rows = []
seen_texts = {}   # deduplicate by text

with open(INPUT, encoding='utf-8') as f:
    for i, line in enumerate(f):
        if MAX_ROWS and i >= MAX_ROWS:
            break
        parts = line.rstrip('\n').split('\t')
        if len(parts) != 3:
            continue
        s1, s2, label = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if label not in ('0', '1'):
            continue

        # sentence1 is always an original source document
        if s1 not in seen_texts:
            seen_texts[s1] = f"src_{len(seen_texts):06d}"
            rows.append({
                'file_name': seen_texts[s1],
                'text':      s1,
                'category':  'original',
                'source':    'snli',
            })

        # sentence2 category depends on label
        if s2 not in seen_texts:
            seen_texts[s2] = f"src_{len(seen_texts):06d}"
            rows.append({
                'file_name': seen_texts[s2],
                'text':      s2,
                'category':  'plagiarized' if label == '1' else 'original',
                'source':    'snli',
            })

with open(OUTPUT, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['file_name', 'text', 'category', 'source'])
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} documents to {OUTPUT}")
