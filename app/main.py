from fastapi import FastAPI
from fastapi.middleware.cors
import CORSMiddleware
import logging
logging.basicConfig(level=logging.INFO)
app = FastAPI(
    title="Nutrifit ChatBot API",
    description="مدرب اللياقة والتغذية الذكي بالذكاء الاصطناعي",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from app.api import auth, chat
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
@app.get("/")
def root():
    return {
        "message": "Welcome to Nutrifit ChatBot API",
        "status": "online",
        "version": "1.0.0"
    }
@app.get("/health")
def health():
    return {"status": "healthy"}
print("🚀 Nutrifit API started successfully!")
