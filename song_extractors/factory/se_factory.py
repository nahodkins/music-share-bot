from song_extractors.am_song_extractor import AppleMusicSongExtractor
from song_extractors.ytm_song_extractor import YoutubeMusicSongExtractor
from util.singleton_meta import SingletonMeta


class SongExtractorsFactory(metaclass=SingletonMeta):

    def __init__(self):
        _am_song_extractor = AppleMusicSongExtractor()
        _ytm_song_extractor = YoutubeMusicSongExtractor()

        self._song_extractors = {
            "Apple Music": _am_song_extractor,
            "YouTube Music": _ytm_song_extractor
        }

    def get_song_extractor(self, service_name):
        return self._song_extractors[service_name]

    def get_extractors_by_exclusion(self, service_to_exclude):
        return {
            service_name: song_extractor
            for service_name, song_extractor
            in self._song_extractors.items()
            if service_name != service_to_exclude
        }
