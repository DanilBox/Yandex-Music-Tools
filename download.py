import datetime
from pathlib import Path
from types import MethodType

from yandex_music import TracksList

from base_client import base_client


def save_json(content: str, object_type: str, date: str = str(datetime.date.today())) -> None:
    track_file = Path(f"tracks/{date}/{object_type}-{date}.json")

    if track_file.exists():
        exit(f"Файл '{track_file.name}' уже существует")

    if not (folder := track_file.parent).exists():
        folder.mkdir(parents=True)

    track_file.write_text(content, encoding="utf-8")


def save_tracks(tracks: TracksList, object_type: str) -> None:
    save_json(tracks.to_json(), object_type)
    print(f"Сохранено '{len(tracks)}' треков типа '{object_type}'!")


def save_wrap(func: MethodType) -> TracksList | None:
    result: TracksList | None = func()
    object_name = func.__name__.replace("users_", "").replace("_tracks", "")

    if result is None:
        exit('Ошибка при получения списка треков')

    save_tracks(result, object_name)
    return result


def main() -> None:
    client = base_client()

    save_wrap(client.users_dislikes_tracks)
    save_wrap(client.users_likes_tracks)


if __name__ == "__main__":
    main()
