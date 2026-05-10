from fastapi import FastAPI
from app.database.database import engine, Base
from app.api import auth, chat
import logging

# تقليل اللوجز بشكل قوي
logging.basicConfig(level=logging.ERROR)

for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.ERROR)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriFit AI Coach API", docs_url="/docs", redoc_url=None)

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "running", "message": "NutriFit API"}
