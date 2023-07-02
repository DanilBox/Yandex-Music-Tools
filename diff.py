import datetime
import json
from functools import cache
from pathlib import Path
from typing import NamedTuple

from yandex_music import Client, Track, TrackShort, TracksList


@cache
def new_client() -> Client:
    return Client()


class DiffResult(NamedTuple):
    added_tracks: list[TrackShort]
    deleted_tracks: list[TrackShort]


def diff_tracks(tracks_from: list[TrackShort], tracks_to: list[TrackShort]) -> DiffResult:
    return DiffResult(
        added_tracks=list(set(tracks_to) - set(tracks_from)),
        deleted_tracks=list(set(tracks_from) - set(tracks_to)),
    )


def get_tracks_by_date(object_type: str, date: str = str(datetime.date.today())) -> list[TrackShort]:
    track_file = Path(f"tracks/{date}/{object_type}-{date}.json")
    if not track_file.exists():
        exit(f"Файла '{track_file.name}' не существует")

    result: TracksList | None = TracksList.de_json(json.loads(track_file.read_text()), new_client())
    if result is None:
        exit("Ошибка при получение списка треков")

    return result.tracks


def get_parent_save_date(this_date: str = str(datetime.date.today())) -> str:
    save_folder = Path("tracks")
    saved_date = [str(path.name) for path in save_folder.iterdir() if path.is_dir()]
    saved_date.sort()

    key = this_date
    if key not in saved_date:
        exit(f"Дамп '{key}' не найден")

    parent_date = saved_date[saved_date.index(key) - 1]
    return parent_date


def diff_object(object_type: str) -> DiffResult:
    this_track = get_tracks_by_date(object_type)
    parent_track = get_tracks_by_date(object_type, get_parent_save_date())

    return diff_tracks(parent_track, this_track)


def track_info(track: Track) -> str:
    artists = " ".join([artist.name for artist in track.artists])
    return f"'{track.title}' by '{artists}'"


def show_diff(result: DiffResult) -> None:
    print("Новые добавленные треки:")
    for new_track in result.added_tracks:
        print(track_info(new_track.fetch_track()))

    print()

    print("Удалённые треки:")
    for del_track in result.deleted_tracks:
        print(track_info(del_track.fetch_track()))

    print()


def show_diff_object(object_type: str) -> None:
    print(f"Разница по объекту {object_type}")
    show_diff(diff_object(object_type))


def main() -> None:
    _ = new_client()

    show_diff_object("likes")
    show_diff_object("dislikes")


if __name__ == "__main__":
    main()
