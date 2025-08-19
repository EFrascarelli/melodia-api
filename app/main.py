from fastapi import FastAPI
from app.database import Base, engine
from app import models

app = FastAPI(
    title="Melodia API",
    description="API REST para gestionar playlists y canciones",
    version="0.1.0",
)

@app.get("/ping")
def ping():
    return {"message": "pong"}

Base.metadata.create_all(bind=engine)
