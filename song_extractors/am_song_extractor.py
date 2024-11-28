import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from song_details.song_details import SongDetails
from song_extractors.song_extractor import SongExtractor

logger = logging.getLogger(__name__)


class AppleMusicSongExtractor(SongExtractor):

    _SONG_NAME_XPATH = ('//div[contains(@class, "songs-list-row--selected")]'
                        '//div[contains(@data-testid, "track-title")]')
    _ARTISTS_XPATH = '//div[contains(@class, "headings__subtitles")]/a'
    _ALBUM_NAME = '//h1[contains(@class, "headings__title")]/span'
    _SEARCH_BAR_XPATH = ("//div[contains(@class, 'top-search-lockup__action')]"
                         "/a")

    def __init__(self):
        self._init_driver()

    def extract_song_details(self, song_url):
        logger.info(f"Extracting song details: {song_url}")
        self.driver.get(song_url)

        artist_names = self._get_artists_name()

        try:
            song_name = (self.driver
                         .find_element(By.XPATH, self._SONG_NAME_XPATH).text)
            is_album = False
        except WebDriverException:
            song_name = (self.driver
                         .find_element(By.XPATH, self._ALBUM_NAME).text)
            is_album = True

        return SongDetails(
            song_name=song_name,
            song_authors=artist_names,
            is_album=is_album
        )

    def get_song_url(self, song_details: SongDetails):
        import urllib.parse
        logger.info(f"Getting song URL by details: {song_details}")

        song_keys = song_details.get_song_keys()
        url = "https://music.apple.com/us/search?term="

        self.driver.get(url + urllib.parse.quote(song_keys))

        song_element = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, self._SEARCH_BAR_XPATH))
        )

        return song_element.get_attribute("href")

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        service = Service('./chromedriver')

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def _get_artists_name(self, retry_count=5, sleep_time=1):
        try:
            artist_name_elements = WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, self._ARTISTS_XPATH))
            ).find_elements(
                By.XPATH, self._ARTISTS_XPATH
            )
            artist_names = [artist.text for artist in artist_name_elements]

            return artist_names
        except WebDriverException as exception:
            if retry_count > 0:
                logger.warning(f"Retrying to get artist names in {sleep_time} seconds.")
                time.sleep(sleep_time)
                return self._get_artists_name(retry_count=retry_count - 1,
                                              sleep_time=sleep_time * 2)
            else:
                raise exception
