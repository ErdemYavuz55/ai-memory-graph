# backend/app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.nlp_triplet import extract_triplets_from_text
from app.services.graph_builder import build_graph_from_triplets, export_graph_as_edges  # ✅ yeni eklendi

router = APIRouter()

class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

@router.post("/extract")
async def extract_triplets(messages: List[Message]):
    all_triplets = []

    for msg in messages:
        extracted = extract_triplets_from_text(msg.text)
        for triplet in extracted:
            triplet["timestamp"] = msg.timestamp
            triplet["author"] = msg.sender
            all_triplets.append(triplet)

    # ✅ Yeni eklenen bölüm: graph oluştur
    graph = build_graph_from_triplets(all_triplets)
    edges = export_graph_as_edges(graph)

    # ✅ Yanıtı hem triplet hem de graph olarak dön
    return {
        "triplets": all_triplets,
        "graph": edges
    }
@router.post("/memory-summary")
async def memory_summary(messages: List[Message]):
    from app.services.memory_engine import (
        group_by_author,
        count_predicates,
        most_common_subjects
    )

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

from fastapi import Query
from app.services.memory_engine import (
    group_by_author,
    count_predicates,
    most_common_subjects,
    get_triplets_by_author,
    get_triplets_by_subject,
    get_triplets_by_predicate,
)

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


