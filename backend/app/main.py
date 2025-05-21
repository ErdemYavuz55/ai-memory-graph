# backend/app/main.py
from fastapi import FastAPI
from app.routes import chat

app = FastAPI(title="AI Memory Graph API")

# Route register
app.include_router(chat.router, prefix="/api/chat")
