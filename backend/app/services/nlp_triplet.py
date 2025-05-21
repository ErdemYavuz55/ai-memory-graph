# backend/app/services/nlp_triplet.py

import spacy
from typing import List, Dict

# Artık gelişmiş modeli kullanıyoruz
nlp = spacy.load("en_core_web_trf")

def extract_triplets_from_text(text: str) -> List[Dict]:
    doc = nlp(text)
    triplets = []

    for sent in doc.sents:
        subject = ""
        verb = ""
        obj = ""

        for token in sent:
            if token.dep_ in ("nsubj", "nsubjpass"):
                subject = token.text
            if token.dep_ in ("dobj", "pobj", "attr"):
                obj = token.text
            if token.head.pos_ == "VERB":
                verb = token.head.lemma_

        if subject and verb and obj:
            triplets.append({
                "subject": subject,
                "predicate": verb,
                "object": obj
            })

    return triplets
