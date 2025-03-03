import datetime
import json
import sys
from pathlib import Path
from types import MethodType

from yandex_music import TracksList

from base_client import base_client


def save_json(content: str, object_type: str, date: str = str(datetime.date.today())) -> None:
    track_file = Path(f"tracks/{date}/{object_type}-{date}.json")

    if track_file.exists():
        sys.exit(f"Файл '{track_file.name}' уже существует")

    if not (folder := track_file.parent).exists():
        folder.mkdir(parents=True)

    track_file.write_text(content, encoding="utf-8")


def save_tracks(tracks: TracksList, object_type: str) -> None:
    if len(tracks) != 0:
        dump = [track.to_dict() for track in tracks.fetch_tracks()]
    else:
        dump = []

    save_json(json.dumps(dump), object_type)
    print(f"Сохранено '{len(tracks)}' треков типа '{object_type}'!")


def save_wrap(func: MethodType) -> TracksList | None:
    result: TracksList | None = func()
    object_name = func.__name__.replace("users_", "").replace("_tracks", "")

    if result is None:
        sys.exit("Ошибка при получения списка треков")

    save_tracks(result, object_name)
    return result


def main() -> None:
    client = base_client()

    save_wrap(client.users_dislikes_tracks)
    save_wrap(client.users_likes_tracks)


if __name__ == "__main__":
    main()
