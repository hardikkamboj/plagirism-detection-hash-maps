from corpus     import load_corpus
from preprocess import preprocess
from similarity import detect_plagiarism

K         = 5     # k-gram size — try 5, 7, 10
THRESHOLD = 0.5   # Jaccard threshold — tune against ground truth labels

# --- phase 1: build index from corpus ---
index, doc_lengths, metadata = load_corpus('corpus.csv', k=K)
print(f"Index built: {len(index)} unique k-gram hashes")

# --- phase 2: query a new document ---
query_text = preprocess("the cat sat on the mat and the cat was happy")

results = detect_plagiarism(query_text, index, doc_lengths, k=K, threshold=THRESHOLD)

if results:
    print("\nPlagiarism detected:")
    for r in results:
        meta = metadata.get(r['doc_id'], {})
        print(f"  {r['doc_id']}  score={r['score']}  category={meta.get('category')}")
else:
    print("\nNo plagiarism detected above threshold.")