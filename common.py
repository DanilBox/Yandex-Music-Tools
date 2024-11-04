import datetime
import json
import sys
from enum import StrEnum
from pathlib import Path

from yandex_music import Track

from base_client import null_client

SAVED_FOLDER = Path("tracks")


class TrackType(StrEnum):
    LIKES = "likes"
    DISLIKES = "dislikes"


def get_date_saved_tracks() -> list[str]:
    saved_date = [str(path.name) for path in SAVED_FOLDER.iterdir() if path.is_dir()]
    saved_date.sort()

    return saved_date


def get_tracks_by_date(object_type: str | TrackType, date: str = str(datetime.date.today())) -> list[Track]:
    track_file = SAVED_FOLDER / Path(f"{date}/{object_type}-{date}.json")
    if not track_file.exists():
        sys.exit(f"Файла '{track_file.name}' не существует")

    data = json.loads(track_file.read_text())
    if len(data) == 0:
        return []

    tracks: list[Track] = Track.de_list(data, null_client())
    return tracks


def get_parent_save_date(this_date: str = str(datetime.date.today())) -> str:
    saved_date = get_date_saved_tracks()

    if this_date not in saved_date:
        sys.exit(f"Дамп '{this_date}' не найден")

    parent_date = saved_date[saved_date.index(this_date) - 1]
    return parent_date
