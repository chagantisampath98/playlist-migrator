from dataclasses import dataclass


@dataclass
class Song:
    title: str
    artist: str
    album: str
    duration_ms: int
    spotify_id: str