from fastapi import FastAPI
from app.database.database import engine, Base
from app.api import auth, chat
import logging

logging.basicConfig(level=logging.ERROR)

app = FastAPI(
    title="Nutrifit ChatBot API",
    description="مدرب اللياقة والتغذية الذكي بالذكاء الاصطناعي",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Nutrifit ChatBot API",
        "status": "online",
        "version": "1.0.0"
    }
