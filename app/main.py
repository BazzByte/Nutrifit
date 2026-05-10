from fastapi import FastAPI
from app.database.database import engine, Base
from app.api import auth, chat
import logging
logging.basicConfig(level=logging.WARNING)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.setLevel(logging.WARNING)
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.setLevel(logging.WARNING)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriFit AI Coach API")

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "NutriFit API is running"}
