import json
import re
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class MusicService:

    service_name: str
    url_regex: str


def extract_url(message: str):
    return re.search("(?P<url>https?://[^\s]+)", message).group("url")


def get_music_service(url: str):
    services: list[MusicService] = _extract_services()

    for service in services:
        if re.search(service.url_regex, url):
            return service.service_name

    return None


def _extract_services(json_path="config/music_services.json"):
    with open(json_path, "r") as file:
        data = json.load(file)

    music_services = [from_dict(data_class=MusicService, data=music_service)
                      for music_service in data]

    return music_services
