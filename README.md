# 🧠 AI Memory Graph

AI-powered memory system that extracts structured knowledge from multi-user group chats. Inspired by [getzep.com](https://getzep.com), this project goes beyond 1:1 chatbot memory by supporting group dialogue, visualization, and structured memory export.

---

## 🚀 Features

* ✅ **Triplet Extraction**: Extracts subject–predicate–object keypoints from user messages using SpaCy's transformer model
* ✅ **Author Attribution**: Every triplet is linked to its author and timestamp
* ✅ **Group Chat Support**: Handles multiple speakers in conversations (not limited to AI+user)
* ✅ **Knowledge Graph Generation**: Builds a visual graph using NetworkX and PyVis
* ✅ **Memory Summary**: Calculates top predicates, subjects, and user-based triplet counts
* ✅ **Memory Query API**: Search triplets by `author`, `predicate`, or `subject`
* ✅ **JSON Memory Export**: Stores memory in a structured format per user

---

## 📁 Project Structure

```
ai-memory-graph/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI server entry point
│   │   ├── routes/chat.py        # API endpoints (/extract, /query, /memory-summary)
│   │   └── services/
│   │       ├── nlp_triplet.py    # Extract triplets using SpaCy
│   │       ├── graph_builder.py  # Create NetworkX graph
│   │       ├── graph_visualizer.py # Visualize graph using PyVis
│   │       └── memory_engine.py  # Query, group, and export memory
│   ├── group_chat_sample.json    # Dummy test data (group chat)
│   ├── analyze_memory.py         # CLI script: Extract + summarize
│   ├── export_memory.py          # CLI script: Export JSON memory
│   └── memory_export.json        # Output memory (grouped by user)
```

---

## 🧪 Example Use Case

### Input Messages

```json
[
  {"sender": "Erdem", "text": "Ali suggested using FastAPI for the backend.", "timestamp": "2025-05-15T10:00:00Z"},
  {"sender": "Ayse", "text": "We should build the UI with React.", "timestamp": "2025-05-15T10:05:00Z"}
]
```

### Triplet Output (via `/api/chat/extract`)

```json
[
  {"subject": "Ali", "predicate": "suggest", "object": "FastAPI", "author": "Erdem", "timestamp": "..."},
  {"subject": "We", "predicate": "build", "object": "React", "author": "Ayse", "timestamp": "..."}
]
```

### Memory Export

```json
{
  "Erdem": [ {"subject": "Ali", "predicate": "suggest", "object": "FastAPI", ...} ],
  "Ayse": [ {"subject": "We", "predicate": "build", "object": "React", ...} ]
}
```

---

## 🔧 Tech Stack

* **Backend**: Python, FastAPI, SpaCy, NetworkX, PyVis
* **NLP Model**: `en_core_web_trf` (Transformer-based for accurate triplet extraction)

---

## 🛠 Setup Instructions

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (Windows)

# Install requirements
pip install -r requirements.txt
python -m spacy download en_core_web_trf

# Run server
python -m uvicorn app.main:app --reload
```

Then open: [http://localhost:8000/docs](http://localhost:8000/docs) to test APIs.

---

## 📌 Motivation

This project is inspired by Zep’s memory system, but extends it to group conversations. Instead of only tracking a chatbot’s interaction with one user, this system works for meetings, group chats, or collaborative logs.

---

## 📤 Author & Credits

👤 Developed by **Erdem Yavuz Hacisoftaoglu** — as part of internship and portfolio development.

If you're viewing this as a recruiter or reviewer:

> ✔️ NLP & FastAPI proficiency
> ✔️ Data structuring, graph logic, memory architecture
> ✔️ End-to-end working system — not a toy demo

---

## 📌 Roadmap (Next Steps)

* [ ] 📆 Date filtering via timestamp range
* [ ] 📥 Load/export memory to JSON (completed ✅ export, pending: import)
* [ ] 🌐 Frontend: graph UI + memory panel
* [ ] 🤖 GPT-based Q\&A interface: e.g. "Who suggested using X?"
* [ ] 📚 Zep-compatible file structure (JSONL chat log + user memory)
* [ ] 🧪 Unit & integration tests
* [ ] 📝 Add Dockerfile for deployment

---

## 📎 License

This project is open-source and MIT licensed.

---

## 🔗 Related

* [Zep - Open Source LLM Memory Server](https://getzep.com)
* [Graphiti - Graph library used by Zep](https://github.com/getzep/graphiti)
