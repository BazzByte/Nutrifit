from fastapi import FastAPI
from app.database.database import engine, Base
from app.api import auth, chat

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriFit AI Coach API")

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Welcome to NutriFit AI Coach API"}
