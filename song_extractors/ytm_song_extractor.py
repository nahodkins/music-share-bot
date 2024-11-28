import logging

from song_details.song_details import SongDetails
from song_extractors.song_extractor import SongExtractor

from ytmusicapi import YTMusic

logger = logging.getLogger(__name__)


class YoutubeMusicSongExtractor(SongExtractor):

    def __init__(self):
        self.yt_music = YTMusic()

    def extract_song_details(self, song_url):
        video_id = self._get_video_id(song_url)

        if video_id:
            found_result = self.yt_music.get_song(video_id)['videoDetails']

            song_name = found_result['title']
            artists = [found_result['author']]
            is_album = False
        else:
            playlist_id = self._get_playlist_id(song_url)
            album_id = self.yt_music.get_album_browse_id(playlist_id)
            found_result = self.yt_music.get_album(album_id)

            song_name = found_result['title']
            artists = [artist['name'] for artist in found_result['artists']]
            is_album = True

        return SongDetails(
            song_name=song_name,
            song_authors=artists,
            is_album=is_album
        )

    def get_song_url(self, song_details: SongDetails):
        found_result = self.yt_music.search(song_details.get_song_keys())[0]

        if song_details.is_album:
            playlist_id = found_result['playlistId']
            song_url = f"https://music.youtube.com/playlist?list={playlist_id}"
        else:
            video_id = found_result['videoId']
            song_url = f'https://music.youtube.com/watch?v={video_id}'

        return song_url

    @staticmethod
    def _get_video_id(song_url):
        import re
        match = re.search(r"v=([^&]+)", song_url)

        if match:
            return match.group(1)
        else:
            return None

    @staticmethod
    def _get_playlist_id(song_url):
        import re
        match = re.search(r"list=([^&]+)", song_url)

        if match:
            return match.group(1)
        else:
            return None
