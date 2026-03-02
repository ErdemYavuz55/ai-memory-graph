# 🧠 AI Memory Graph

AI-powered memory system that extracts structured knowledge from multi-user group chats. Inspired by [getzep.com](https://getzep.com), this project goes beyond 1:1 chatbot memory by supporting group dialogue, visualization, and structured memory export.

---

## 🔧 Tech Stack

* **Backend**: Python, FastAPI, SpaCy, NetworkX, PyVis
* **NLP Model**: `en_core_web_trf` (Transformer-based for accurate triplet extraction)

---

## 🚀 Live Demo
You can try the model directly in your browser without installing anything: 
**[👉 Click here to open the Web App](https://huggingface.co/spaces/erdemyavuz/ai_memory_graph)**

## ✨ New Features

The project was extended with several new capabilities:

- ✅ Natural language question answering (`/qa`) — Ex: *“Kim MongoDB’yi seviyor?”*
- ✅ Triplet update functionality via `PUT /triplet/update/{id}`
- ✅ Triplet deletion via `DELETE /triplet/delete/{id}`
- ✅ UUID-based unique triplet identification
- ✅ Live-editable JSON memory file (`memory_export.json`) with real-time effect

These changes enable a dynamic and editable memory graph structure.

---

## 📤 Author & Credits

👤 Developed by **Erdem Yavuz Hacisoftaoglu** — as part of internship and portfolio development.

If you're viewing this as a recruiter or reviewer:

> ✔️ NLP & FastAPI proficiency  
> ✔️ Data structuring, graph logic, memory architecture  
> ✔️ End-to-end working system — not a toy demo

---

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
│   │   ├── routes/chat.py        # API endpoints (extract, query, memory-summary, qa, update, delete)
│   │   └── services/
│   │       ├── nlp_triplet.py    # Extract triplets using SpaCy
│   │       ├── graph_builder.py  # Create NetworkX graph
│   │       ├── graph_visualizer.py # Visualize graph using PyVis
│   │       └── memory_engine.py  # Query, group, update, delete, and export memory
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
* Support live memory editing (update, delete)

---

### 🧩 How We Achieved This

| Functionality          | How We Implemented It                                                       | Where in Code                                              |
| ---------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 🔍 Triplet Extraction  | Using SpaCy Transformer model to extract subject–predicate–object from text | `services/nlp_triplet.py`                                  |
| 🧠 User-Based Memory   | Grouping extracted triplets by sender and timestamp                         | `services/memory_engine.py`                                |
| 📊 Statistical Summary | Counting total triplets, predicates, subjects, grouped by user              | `services/memory_engine.py` and `/memory-summary` endpoint |
| 🔎 Memory Search       | Query memory by predicate, subject or author                                | `services/memory_engine.py` and `/query` endpoint          |
| 🧠 QA Answering        | Extract answers from memory using natural language filters                  | `routes/chat.py` and `/qa` endpoint                        |
| ✏️ Memory Update       | Update memory using `PUT` and triplet ID                                     | `routes/chat.py` and `/triplet/update/{id}`                |
| 🗑️ Memory Deletion     | Delete memory entries using `DELETE` by ID                                   | `routes/chat.py` and `/triplet/delete/{id}`                |
| 🌐 API Interface       | Built with FastAPI for accessible usage                                     | `routes/chat.py`, `main.py`                                |
| 📈 Knowledge Graph     | Convert triplets to visual graphs using NetworkX + PyVis                    | `services/graph_builder.py`, `graph_visualizer.py`         |
| 💾 Export to JSON      | Memory data can be exported per user                                        | `export_memory.py` script                                  |

---

## 🛠 Setup Instructions

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_trf
```

---

## 🧪 How to Try the Project

1. **Start the Server**
```bash
cd backend
uvicorn app.main:app --reload
```

2. **Go to Swagger UI**
[http://localhost:8000/docs](http://localhost:8000/docs)

3. **Use Endpoints:**
- `/extract`: Extract triplets from messages
- `/memory-summary`: Get stats about memory
- `/query`: Filter memory
- `/qa`: Ask a question (ex: “Erdem ne dedi?”)
- `/triplet/update/{id}`: Update existing memory item
- `/triplet/delete/{id}`: Remove triplet from memory

---

## 📎 License

MIT

---

## 🔗 Related

* [Zep - Open Source LLM Memory Server](https://getzep.com)
* [Graphiti - Graph library used by Zep](https://github.com/getzep/graphiti)
