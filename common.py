import datetime
import json
from enum import StrEnum
from pathlib import Path

from yandex_music import Track

from base_client import null_client


class TrackType(StrEnum):
    LIKES = "likes"
    DISLIKES = "dislikes"


def get_tracks_by_date(object_type: str | TrackType, date: str = str(datetime.date.today())) -> list[Track]:
    track_file = Path(f"tracks/{date}/{object_type}-{date}.json")
    if not track_file.exists():
        exit(f"Файла '{track_file.name}' не существует")

    data = json.loads(track_file.read_text())
    if len(data) == 0:
        return []

    tracks: list[Track] = Track.de_list(data, null_client())
    return tracks


def get_parent_save_date(this_date: str = str(datetime.date.today())) -> str:
    save_folder = Path("tracks")
    saved_date = [str(path.name) for path in save_folder.iterdir() if path.is_dir()]
    saved_date.sort()

    key = this_date
    if key not in saved_date:
        exit(f"Дамп '{key}' не найден")

    parent_date = saved_date[saved_date.index(key) - 1]
    return parent_date
