from fastapi import FastAPI

app = FastAPI(
    title="Melodia API",
    description="API REST para gestionar playlists y canciones",
    version="0.1.0",
)

@app.get("/ping")
def ping():
    return {"message": "pong"}
