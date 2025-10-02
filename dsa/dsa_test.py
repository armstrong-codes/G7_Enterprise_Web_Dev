import json, time, random
from pathlib import Path

def linear_search(transactions, target_id):
    for t in transactions:
        if t["id"] == target_id:
            return t
    return None

def dict_lookup(index, target_id):
    return index.get(target_id)

def build_index(transactions):
    return {t["id"]: t for t in transactions}

if __name__ == "__main__":
    p = Path(__file__).parent / "transactions.json"
    tx = json.loads(p.read_text(encoding="utf-8"))
    # If less than 20, duplicate to get 50 entries for timings
    if len(tx) < 50:
        base = tx.copy()
        next_id = len(tx)+1
        while len(tx) < 50:
            for item in base:
                new = dict(item)
                new["id"] = str(next_id)
                tx.append(new)
                next_id += 1
                if len(tx) >= 50:
                    break
    # Build index (dictionary)
    index = build_index(tx)
    # Pick 20 random ids to search for (existing)
    ids = random.sample([t["id"] for t in tx], 20)

    # Number of iterations to amplify timings
    ITER = 1000

    ls_time = 0.0
    dl_time = 0.0

    for _ in range(ITER):
        for target in ids:
            start = time.perf_counter()
            linear_search(tx, target)
            ls_time += time.perf_counter() - start

            start = time.perf_counter()
            dict_lookup(index, target)
            dl_time += time.perf_counter() - start

    print(f"Linear search total time over {ITER}*{len(ids)} searches: {ls_time:.6f} seconds")
    print(f"Dict lookup total time over {ITER}*{len(ids)} searches:   {dl_time:.6f} seconds")
    print(f"Average linear per lookup: {ls_time/(ITER*len(ids)):.9f}s")
    print(f"Average dict per lookup:   {dl_time/(ITER*len(ids)):.9f}s")
    print("Dictionary lookup is faster because it uses O(1) average-time hashing lookup, while linear search is O(n).")