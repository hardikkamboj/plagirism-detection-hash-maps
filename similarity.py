from hash_index import rolling_hashes


def get_matches(query_hashes: list[int],
                index: dict[int, set]) -> dict[str, int]:
    """
    For each hash in the query, look up which docs contain it.
    Returns { doc_id: count_of_shared_hashes }
    """
    matches = {}
    for h in query_hashes:
        if h in index:                       # O(1) lookup
            for doc_id in index[h]:
                matches[doc_id] = matches.get(doc_id, 0) + 1
    return matches


def jaccard(shared: int, query_total: int, source_total: int) -> float:
    union = query_total + source_total - shared
    if union == 0:
        return 0.0
    return shared / union


def detect_plagiarism(query_text: str,
                      index: dict[int, set],
                      doc_lengths: dict[str, int],
                      k: int = 5,
                      threshold: float = 0.5) -> list[dict]:
    """
    Returns list of { doc_id, score } for all docs above threshold,
    sorted by score descending.
    """
    q_hashes = rolling_hashes(query_text, k)
    q_total  = len(q_hashes)
    matches  = get_matches(q_hashes, index)

    results = []
    for doc_id, shared in matches.items():
        score = jaccard(shared, q_total, doc_lengths[doc_id])
        if score >= threshold:
            results.append({ 'doc_id': doc_id, 'score': round(score, 4) })

    return sorted(results, key=lambda x: x['score'], reverse=True)