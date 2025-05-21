from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
import os
import json

from app.services.nlp_triplet import extract_triplets_from_text
from app.services.graph_builder import build_graph_from_triplets, export_graph_as_edges
from app.services.memory_engine import (
    group_by_author,
    count_predicates,
    most_common_subjects,
    get_triplets_by_author,
    get_triplets_by_subject,
    get_triplets_by_predicate,
    query_memory,
)

router = APIRouter()


class Message(BaseModel):
    sender: str
    text: str
    timestamp: str


# ----------------------------------------------------------
# Triplet Extraction
# ----------------------------------------------------------
@router.post("/extract")
async def extract_triplets(messages: List[Message]):
    all_triplets = []

    for msg in messages:
        extracted = extract_triplets_from_text(msg.text)
        for triplet in extracted:
            triplet["timestamp"] = msg.timestamp
            triplet["author"] = msg.sender
            all_triplets.append(triplet)

    graph = build_graph_from_triplets(all_triplets)
    edges = export_graph_as_edges(graph)

    return {
        "triplets": all_triplets,
        "graph": edges
    }


# ----------------------------------------------------------
# Triplet Statistics Summary
# ----------------------------------------------------------
@router.post("/memory-summary")
async def memory_summary(messages: List[Message]):
    all_triplets = []

    for msg in messages:
        extracted = extract_triplets_from_text(msg.text)
        for triplet in extracted:
            triplet["timestamp"] = msg.timestamp
            triplet["author"] = msg.sender
            all_triplets.append(triplet)

    summary = {
        "total_triplets": len(all_triplets),
        "by_user": group_by_author(all_triplets),
        "predicate_counts": count_predicates(all_triplets),
        "common_subjects": most_common_subjects(all_triplets)
    }

    return summary


# ----------------------------------------------------------
# Triplet Query (Filtered)
# ----------------------------------------------------------
@router.post("/query")
async def query_triplets(
    messages: List[Message],
    author: str = Query(None),
    subject: str = Query(None),
    predicate: str = Query(None)
):
    all_triplets = []

    for msg in messages:
        extracted = extract_triplets_from_text(msg.text)
        for triplet in extracted:
            triplet["timestamp"] = msg.timestamp
            triplet["author"] = msg.sender
            all_triplets.append(triplet)

    filtered = all_triplets

    if author:
        filtered = get_triplets_by_author(filtered, author)
    if subject:
        filtered = get_triplets_by_subject(filtered, subject)
    if predicate:
        filtered = get_triplets_by_predicate(filtered, predicate)

    return {
        "total_triplets": len(filtered),
        "results": filtered
    }


# ----------------------------------------------------------
# Natural Language QA over Memory
# ----------------------------------------------------------
@router.get("/qa")
async def qa_query(question: str = Query(..., description="Doğal dilde soru girin")):
    filters = extract_query_from_question(question)
    memory = load_memory()

    print("🚀 SORU:", question)
    print("🔍 FILTERS:", filters)

    results = query_memory(
        memory,
        author=filters.get("author"),
        predicate=filters.get("predicate"),
        subject=filters.get("subject"),
        object_=filters.get("object"),
    )

    print("📦 SONUÇ TRIPLETLER:", results)

    answer = format_answer_smart(results, filters)

    return {
        "soru": question,
        "filters": filters,
        "cevap": answer,
        "triplet_sayisi": len(results),
        "tripletler": results
    }



@router.delete("/triplet/delete/{triplet_id}")
async def delete_triplet(triplet_id: str):
    memory = load_memory()
    changed = False

    for author, triplets in memory.items():
        original_count = len(triplets)
        memory[author] = [t for t in triplets if t.get("id") != triplet_id]
        if len(memory[author]) < original_count:
            changed = True

    if changed:
        _save_memory(memory)
        return {"status": "deleted", "id": triplet_id}
    else:
        return {"status": "not found", "id": triplet_id}



@router.put("/triplet/update/{triplet_id}")
async def update_triplet(triplet_id: str, updated_fields: dict):
    memory = load_memory()
    updated = False

    for author, triplets in memory.items():
        for t in triplets:
            if t.get("id") == triplet_id:
                t.update(updated_fields)  # ✅ güncellenen alanları uygula
                updated = True
                break

    if updated:
        _save_memory(memory)
        return {"status": "updated", "id": triplet_id, "new_data": updated_fields}
    else:
        return {"status": "not found", "id": triplet_id}




# ----------------------------------------------------------
# Helpers
# ----------------------------------------------------------
def extract_query_from_question(question: str) -> dict:
    filters = {}
    q = question.lower()

    # --- AUTHOR eşleştirmeleri ---
    if "ayşe" in q:
        filters["author"] = "Ayşe"
    if "erdem" in q:
        filters["author"] = "Erdem"
    if "ali" in q:
        filters["author"] = "Ali"
        
    if "ne dedi" in q:
        filters["return"] = "triplet"
        return filters  # erken çık

    # --- SUBJECT eşleştirmeleri ---
    if "redis" in q:
        filters["subject"] = "Redis"
    if "react" in q:
        filters["subject"] = "React"
    if "fastapi" in q:
        filters["subject"] = "FastAPI"
    if "we" in q:
        filters["subject"] = "we"
    if "ben" in q or (" i " in q):  # boşluklarla eşleştir, yanlış anlamasın
        filters["subject"] = "I"


    # --- OBJECT eşleştirmeleri ---
    if "mongodb" in q:
        filters["object"] = "MongoDB"
    if "ui" in q:
        filters["object"] = "UI"
    if "data" in q:
        filters["object"] = "data"
    if "joins" in q:
        filters["object"] = "joins"
    if "backend" in q:
        filters["object"] = "backend"

    # --- PREDICATE eşleştirmeleri ---
    if "öner" in q or "tavsiye" in q:
        filters["predicate"] = "suggest"
    if "seviyor" in q or "sever" in q or "beğen" in q:
        filters["predicate"] = "like"
    if "destekliyor" in q or "destek" in q:
        filters["predicate"] = "support"
    if "düşünüyor" in q or "düşün" in q:
        filters["predicate"] = "think"
    if "önbellek" in q or "cache" in q:
        filters["predicate"] = "cache"

    # --- Geri dönüş tipi ---
    if "ne dedi" in q or "kim ne dedi" in q:
        filters["return"] = "triplet"
    if "kim" in q:
        filters["return"] = "subject"

    return filters



def format_answer_smart(triplets: list, filters: dict) -> str:
    if not triplets:
        return "Üzgünüm, bu soruya dair bir bilgi bulamadım."

    return_type = filters.get("return")
    messages = []

    for triplet in triplets:
        subj = triplet.get("subject")
        pred = triplet.get("predicate")
        obj = triplet.get("object")
        author = triplet.get("author")

        if return_type == "subject":
            messages.append(f"{obj} ile ilgili eylemi gerçekleştiren kişi: {subj}")
        elif return_type == "triplet":
            messages.append(f"{author} dedi ki: \"{subj} {pred} {obj}\"")
        else:
            sentence = f"{author} dedi ki: \"{subj} {pred} {obj}\""
            messages.append(sentence)

    return "\n".join(messages)


def load_memory():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # backend/app/routes/
    full_path = os.path.abspath(os.path.join(base_dir, "..", "..", "memory_export.json"))
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
    
def _save_memory(memory: dict):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.abspath(os.path.join(base_dir, "..", "..", "memory_export.json"))
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

