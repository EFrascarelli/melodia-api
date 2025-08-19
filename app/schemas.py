from pydantic import BaseModel, Field
from typing import Optional

class SongBase(BaseModel):
    title: str = Field(..., min_length=1)
    artist: str = Field(..., min_length=1)

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int

    class Config:
        orm_mode = True

class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=1)

class PlaylistCreate(PlaylistBase):
    song_ids: Optional[list[int]] = []

class Playlist(PlaylistBase):
    id: int
    songs: list[Song] = []

    class Config:
        orm_mode = True
