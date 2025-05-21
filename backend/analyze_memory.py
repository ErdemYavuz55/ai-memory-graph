import json
from app.services.nlp_triplet import extract_triplets_from_text
from app.services.graph_builder import build_graph_from_triplets
from app.services.memory_engine import group_by_author, count_predicates, most_common_subjects

with open("group_chat_sample.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

all_triplets = []

for msg in messages:
    extracted = extract_triplets_from_text(msg["text"])
    for triplet in extracted:
        triplet["timestamp"] = msg["timestamp"]
        triplet["author"] = msg["sender"]
        all_triplets.append(triplet)

# Hafıza analizleri
by_user = group_by_author(all_triplets)
predicate_stats = count_predicates(all_triplets)
common_subjects = most_common_subjects(all_triplets)

# Çıktı
print("\n🔍 Triplet Sayısı:", len(all_triplets))
print("\n👥 Kullanıcı Bazlı Triplet Hafızası:")
for user, data in by_user.items():
    print(f"  - {user}: {len(data)} triplet")

print("\n🧠 En Çok Geçen Fiiller (Predicates):", predicate_stats)
print("\n📌 En Çok Geçen Özneler (Subjects):", common_subjects)
