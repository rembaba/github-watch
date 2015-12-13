def get_new_entries(cache, new):
    """Compare a new record with cached records and return the new entries
    in the new record
    """
    _new_entries = []
    cached_ids = [r["id"] for r in cache]
    for record in new:
        if record["id"] not in cached_ids:
            _new_entries.append(record)
    return _new_entries

