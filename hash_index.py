M = 1_000_003   # large prime — keeps hash values in range, minimizes collisions
P = 31          # base prime for polynomial hashing


def get_kgrams(text: str, k: int) -> list[str]:
    if len(text) < k:
        return []                             # doc too short — skip
    return [text[i:i+k] for i in range(len(text) - k + 1)]


def rolling_hashes(text: str, k: int) -> list[int]:
    if len(text) < k:
        return []

    # compute first hash from scratch — only time we do O(k) work
    h = 0
    pk = 1                                   # will hold P^(k-1) mod M
    for i in range(k):
        h = (h + ord(text[i]) * pow(P, i, M)) % M
    for i in range(k - 1):
        pk = (pk * P) % M                    # precompute P^(k-1)

    hashes = [h]

    # every subsequent hash is O(1) — rolling update
    for i in range(1, len(text) - k + 1):
        out_char = ord(text[i - 1])          # character leaving the window
        in_char  = ord(text[i + k - 1])     # character entering the window
        h = ((h - out_char + M) % M * P % M + in_char * pk) % M
        hashes.append(h)

    return hashes


def build_index(documents: dict[str, str], k: int = 5) -> dict[int, set]:
    """
    documents: { doc_id: preprocessed_text }
    returns:   { hash_value: {doc_id, doc_id, ...} }
    """
    index = {}
    for doc_id, text in documents.items():
        for h in rolling_hashes(text, k):
            if h not in index:
                index[h] = set()
            index[h].add(doc_id)
    return index