# Plagiarism Detection using Rabin-Karp & Jaccard Similarity

A document-level plagiarism detection system built on Rabin-Karp rolling hashes and Jaccard similarity. Designed for CMSC 606 at UMD.

---

## How It Works

1. **Preprocess** — lowercase, strip punctuation, normalize whitespace
2. **Hash** — slide a window of size `k` over each document, computing a rolling hash (Rabin-Karp) at every position in O(1) per step
3. **Index** — build an inverted index: `{ hash → set of doc_ids }`
4. **Query** — hash the query document, look up each hash in the index, count shared hashes per candidate doc
5. **Score** — compute Jaccard similarity: `|shared| / |union|`; flag docs above a configurable threshold

```
query doc ──► rolling hashes ──► index lookup ──► Jaccard score ──► flagged matches
```

---

## Project Structure

```
.
├── preprocess.py       # Text cleaning (lowercase, remove punctuation)
├── hash_index.py       # Rabin-Karp rolling hash + inverted index builder
├── similarity.py       # Hash matching + Jaccard similarity scorer
├── corpus.py           # CSV corpus loader → index + metadata
├── detector.py         # Main entry point — build index, run a query
├── generate_corpus.py  # Synthetic corpus generator from Project Gutenberg
└── README.md
```

---

## Quickstart

### 1. Generate the corpus

Downloads 3 public-domain books from Project Gutenberg, splits them into 150-word chunks, and creates verbatim plagiarised copies (30% of docs).

```bash
python generate_corpus.py
# → writes corpus.csv (~3,000 docs: ~2,400 original + ~700 plagiarised)
```

> `corpus.csv` is excluded from version control (see `.gitignore`). Re-generate it locally before running.

### 2. Run the detector

```bash
python detector.py
```

To test with a known plagiarised passage, replace `query_text` in `detector.py` with any text from the corpus.

---

## corpus.csv Format

| Column | Description |
|---|---|
| `file_name` | Unique document ID (e.g. `moby_dick_0042`) |
| `text` | Raw document text |
| `category` | Ground truth label: `original` or `plagiarized` |
| `source` | Origin book / source doc ID |

---

## Key Parameters

| Parameter | Default | Effect |
|---|---|---|
| `k` | `5` | K-gram size — smaller = more sensitive, larger = fewer false positives |
| `threshold` | `0.5` | Jaccard threshold — lower = more matches flagged |
| `CHUNK_WORDS` | `150` | Words per chunk in synthetic corpus |
| `PLAGIARISM_RATE` | `0.3` | Fraction of corpus that is plagiarised |

---

## Algorithm Details

**Rolling Hash (Rabin-Karp)**
```
h = Σ ord(char[i]) * P^i  mod M
```
- Base `P = 31`, modulus `M = 1,000,003`
- Each subsequent hash computed in O(1) by sliding the window

**Jaccard Similarity**
```
J(Q, D) = |shared k-gram hashes| / (|Q| + |D| - |shared|)
```

Overall complexity: index build is O(N·L) for N docs of average length L; each query is O(L) for hashing + O(matches) for scoring.

---

## Dependencies

Standard library only — no `pip install` required.

```
Python 3.10+
```
