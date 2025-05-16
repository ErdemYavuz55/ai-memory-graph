# 🧠 AI Memory Graph

AI-powered memory system that extracts structured knowledge from multi-user group chats. Inspired by [getzep.com](https://getzep.com), this project goes beyond 1:1 chatbot memory by supporting group dialogue, visualization, and structured memory export.

---
## 📤 Author & Credits

👤 Developed by **Erdem Yavuz Hacisoftaoglu** — as part of internship and portfolio development.

If you're viewing this as a recruiter or reviewer:

> ✔️ NLP & FastAPI proficiency
> ✔️ Data structuring, graph logic, memory architecture
> ✔️ End-to-end working system — not a toy demo

## 📌 Background & Requirement Context

This project was developed as part of an internship task inspired by the [getzep.com](https://getzep.com) architecture.

Zep extracts structured keypoints from conversation history between an AI chatbot and a single user. However, in many real-world cases, conversations occur in **multi-user group chats** (e.g., team discussions, meetings, etc.). The goal here was to replicate and **extend** Zep's capabilities to support:

* Group chats involving **multiple users**, not just 1:1 chatbot dialogue
* Extraction of **key information (triplets)** from each speaker's message
* **Graph-based memory** of “who said what and when”
* **Visual knowledge representation** inspired by Zep's open-source Graphiti framework ([github.com/getzep/graphiti](https://github.com/getzep/graphiti))

This implementation first began with single-user conversations (just like Zep), and was extended into **dummy group chat testing** to simulate real multi-user discussions.

The ultimate purpose is to **retrieve and summarize past group knowledge** through structured memory and make that memory easy to search, analyze, or visualize.

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



## 🎯 Project Objective & Solution Overview

### 🎯 Goal

To build a structured memory system for group conversations that allows us to:

* Identify **who said what and when**
* Extract meaningful insights from messages (subject–predicate–object)
* Store these insights in a format that is **machine-readable** and **queryable**
* Visualize relationships as a **knowledge graph**

### 🧩 How We Achieved This

| Functionality          | How We Implemented It                                                       | Where in Code                                              |
| ---------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 🔍 Triplet Extraction  | Using SpaCy Transformer model to extract subject–predicate–object from text | `services/nlp_triplet.py`                                  |
| 🧠 User-Based Memory   | Grouping extracted triplets by sender and timestamp                         | `services/memory_engine.py`                                |
| 📊 Statistical Summary | Counting total triplets, predicates, subjects, grouped by user              | `services/memory_engine.py` and `/memory-summary` endpoint |
| 🔎 Memory Search       | Query memory by predicate, subject or author                                | `services/memory_engine.py` and `/query` endpoint          |
| 🌐 API Interface       | Built with FastAPI for accessible usage                                     | `routes/chat.py`, `main.py`                                |
| 📈 Knowledge Graph     | Convert triplets to visual graphs using NetworkX + PyVis                    | `services/graph_builder.py`, `graph_visualizer.py`         |
| 💾 Export to JSON      | Memory data can be exported per user                                        | `export_memory.py` script                                  |

### 🛠 Real-World Use Scenarios

* Meeting summaries ("Who proposed what?")
* AI assistant memory ("Remind me who built the frontend?")
* Organizational knowledge base from team chat logs

## 🛠 Setup Instructions

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate (Windows)

# Install requirements
pip install -r requirements.txt
python -m spacy download en_core_web_trf


### 🧪 How to Try the Project End-to-End (Real Data Testing Guide)

1. **Start the Server**

```bash
cd backend
uvicorn app.main:app --reload
```

2. **Go to Swagger UI**

Open browser at: [http://localhost:8000/docs](http://localhost:8000/docs)

3. **Test the `/extract` Endpoint**

* Click on `POST /extract` → **Try it out**
* Paste your own conversation:

```json
[
  {"sender": "Ali", "text": "I think we should use FastAPI for backend.", "timestamp": "2025-05-15T10:00:00Z"},
  {"sender": "Ayşe", "text": "We can design the UI with Figma.", "timestamp": "2025-05-15T10:05:00Z"}
]
```

* Click **Execute** and check the extracted triplets

4. **Test the `/memory-summary` Endpoint**

* Click `GET /memory-summary` → **Try it out** → **Execute**
* View:

  * How many triplets were extracted
  * Who said how many things
  * Most common actions and subjects

5. **Test the `/query` Endpoint**

* Click `GET /query` → **Try it out**
* Try different filters:

  * `author=Ali`
  * `predicate=use`
  * `subject=We`
* Useful for building a smart assistant memory search

6. **Run from CLI with Real Data**

* Edit `group_chat_sample.json` with real conversation history
* Then run:

```bash
python analyze_memory.py
python export_memory.py
python test_graph_output.py
```

* You will get memory summary in terminal and `triplet_graph.html` in browser

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



## 📌 Roadmap (Next Steps)

* [ ] 📆 Date filtering via timestamp range
* [x] 📥 Load/export memory to JSON (export completed)
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
