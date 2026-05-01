from sentence_transformers import SentenceTransformer, util

print("Loading MiniLM model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("MiniLM ready!")

def get_change_score(old_text: str, new_text: str) -> float:
    """
    0.0 = exactly same
    1.0 = completely different
    """
    if not old_text or not new_text:
        return 1.0

    emb1 = model.encode(old_text[:512])
    emb2 = model.encode(new_text[:512])

    similarity = util.cos_sim(emb1, emb2).item()
    change_score = 1.0 - similarity

    return round(change_score, 3)