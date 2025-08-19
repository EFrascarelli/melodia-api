from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Melodia API",
    description="API REST para gestionar playlists y canciones",
    version="0.1.0",
)
@app.post("/songs", response_model=schemas.Song, status_code=status.HTTP_201_CREATED)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = models.Song(title=song.title, artist=song.artist)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


@app.post("/playlists", response_model=schemas.Playlist, status_code=status.HTTP_201_CREATED)
def create_playlist(playlist: schemas.PlaylistCreate, db: Session = Depends(get_db)):
    db_playlist = models.Playlist(name=playlist.name)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)

    # Agregar canciones si se pasaron song_ids
    if playlist.song_ids:
        for i, song_id in enumerate(playlist.song_ids):
            song = db.query(models.Song).filter(models.Song.id == song_id).first()
            if not song:
                raise HTTPException(status_code=404, detail=f"Song ID {song_id} not found")
            link = models.PlaylistSong(
                playlist_id=db_playlist.id,
                song_id=song_id,
                position=i
            )
            db.add(link)
        db.commit()

    return {
        "id": db_playlist.id,
        "name": db_playlist.name,
        "songs": db_playlist.ordered_songs
    }



@app.get("/songs", response_model=list[schemas.Song])
def get_songs(db: Session = Depends(get_db)):
    return db.query(models.Song).all()

@app.get("/songs/{id}", response_model=schemas.Song)
def get_song(id: int, db: Session = Depends(get_db)):
    song = db.query(models.Song).filter(models.Song.id == id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.get("/playlists", response_model=list[schemas.Playlist])
def get_playlists(db: Session = Depends(get_db)):
    playlists = db.query(models.Playlist).all()
    result = []

    for playlist in playlists:
        ordered_songs = [ps.song for ps in sorted(playlist.songs, key=lambda ps: ps.position)]
        result.append({
            "id": playlist.id,
            "name": playlist.name,
            "songs": ordered_songs
        })

    return result

@app.get("/playlists/{id}", response_model=schemas.Playlist)
def get_playlist(id: int, db: Session = Depends(get_db)):
    playlist = db.query(models.Playlist).filter(models.Playlist.id == id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    ordered_songs = [ps.song for ps in sorted(playlist.songs, key=lambda ps: ps.position)]
    
    return {
        "id": playlist.id,
        "name": playlist.name,
        "songs": ordered_songs
    }

Base.metadata.create_all(bind=engine)
