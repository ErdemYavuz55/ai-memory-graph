from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import memory_routes

app = FastAPI()

# CORS (UI veya farklı origin’den çağrı için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ilk aşamada geniş bırak
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root path: 200 OK döndürsün (Render health probe vs. için)
@app.get("/")
def root():
    return {"status": "ok", "service": "ai-memory-graph"}

# Health endpoint (kontrol için)
@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# burada routerı app’e ekliyoruz
app.include_router(memory_routes.router, prefix="/memory", tags=["Memory"])
