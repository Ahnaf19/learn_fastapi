def next_id(db: dict) -> int:
    """Return the next available integer ID for an in-memory dict-based store."""
    return max(db.keys(), default=0) + 1
