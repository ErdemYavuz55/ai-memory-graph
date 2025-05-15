import json
from app.services.nlp_triplet import extract_triplets_from_text
from app.services.memory_engine import export_memory_to_json

with open("group_chat_sample.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

all_triplets = []

for msg in messages:
    extracted = extract_triplets_from_text(msg["text"])
    for triplet in extracted:
        triplet["timestamp"] = msg["timestamp"]
        triplet["author"] = msg["sender"]
        all_triplets.append(triplet)

export_memory_to_json(all_triplets)
print("✅ memory_export.json dosyası başarıyla oluşturuldu.")
