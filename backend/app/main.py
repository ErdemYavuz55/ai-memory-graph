from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Router importu
from app.routes import chat   # <--- chat.py dosyan buradan geliyor

app = FastAPI(
    title="AI Memory Graph",
    version="0.1.0",
    description="Triplet extraction, graph, query & QA"
)

# CORS (UI veya farklı origin’den çağrı için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ilk aşamada geniş bırak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Chat router'ını ekle
app.include_router(chat.router, prefix="", tags=["memory-graph"])

# ✅ Root path: GET + HEAD
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok", "service": "ai-memory-graph"}

# Health endpoint (kontrol için)
@app.get("/healthz")
def healthz():
    return {"status": "ok"}
