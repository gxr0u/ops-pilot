def compute_confidence(extracted: dict) -> float:
    score = 1.0

    if not extracted.get("decisions"):
        score -= 0.2

    for item in extracted.get("action_items", []):
        if "priority" not in item:
            score -= 0.1

    return min(max(score, 0.0), 0.95)


