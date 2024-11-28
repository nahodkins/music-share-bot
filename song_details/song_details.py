from dataclasses import dataclass


@dataclass
class SongDetails:

    song_name: str
    song_authors: list[str]
    is_album: bool

    def get_song_keys(self):
        return f"{self.song_name} {', '.join(self.song_authors)}"
