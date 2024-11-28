from abc import abstractmethod

from song_details.song_details import SongDetails


class SongExtractor:

    @abstractmethod
    def extract_song_details(self, song_url):
        pass

    @abstractmethod
    def get_song_url(self, song_details: SongDetails):
        pass
