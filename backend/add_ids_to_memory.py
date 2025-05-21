# backend/add_ids_to_memory.py

import json
import uuid
import os

def main():
    # memory_export.json yolunu dinamik oluştur
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "memory_export.json")

    # Dosyayı yükle
    with open(path, "r", encoding="utf-8") as f:
        memory = json.load(f)

    # Her triplete id ekle (varsa atla)
    for author, triplets in memory.items():
        for t in triplets:
            if "id" not in t:
                t["id"] = str(uuid.uuid4())

    # Geri kaydet
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

    print("✅ memory_export.json dosyasına id'ler eklendi.")

if __name__ == "__main__":
    main()
