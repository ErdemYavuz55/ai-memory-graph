from typing import List, Dict
from collections import defaultdict

def group_by_author(triplets: List[Dict]) -> Dict[str, List[Dict]]:
    memory = defaultdict(list)
    for t in triplets:
        memory[t["author"]].append(t)
    return dict(memory)

def count_predicates(triplets: List[Dict]) -> Dict[str, int]:
    counts = defaultdict(int)
    for t in triplets:
        counts[t["predicate"]] += 1
    return dict(counts)

def most_common_subjects(triplets: List[Dict], top_n=3) -> List[str]:
    counts = defaultdict(int)
    for t in triplets:
        counts[t["subject"]] += 1
    sorted_subjects = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_subjects[:top_n]]

def get_triplets_by_author(triplets: List[Dict], author: str) -> List[Dict]:
    return [t for t in triplets if t.get("author", "").lower() == author.lower()]

def get_triplets_by_subject(triplets: List[Dict], subject: str) -> List[Dict]:
    return [t for t in triplets if t.get("subject", "").lower() == subject.lower()]

def get_triplets_by_predicate(triplets: List[Dict], predicate: str) -> List[Dict]:
    return [t for t in triplets if t.get("predicate", "").lower() == predicate.lower()]

import json

def export_memory_to_json(triplets: List[Dict], output_path="memory_export.json") -> None:
    from collections import defaultdict
    memory = defaultdict(list)

    for t in triplets:
        author = t.get("author", "unknown")
        memory[author].append({
            "subject": t["subject"],
            "predicate": t["predicate"],
            "object": t["object"],
            "timestamp": t["timestamp"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

