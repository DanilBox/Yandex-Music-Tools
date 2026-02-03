from functools import cache
from typing import TYPE_CHECKING

from common import TrackType, get_date_saved_tracks
from config import get_config_section
from diff import diff_tracks, get_track_info

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from yandex_music import Track


@cache
def get_tracks_by_date(date: str) -> Sequence[Track]:
    """В обычной ситуации такой кейс не нужен. Сделано из-за повторного получения треков"""
    import common

    return common.get_tracks_by_date(TrackType.LIKES, date)


def grouping_dates(saved_folder: list[str]) -> Iterator[tuple[str, str]]:
    for idx, el in enumerate(saved_folder[:-1]):
        yield el, saved_folder[idx + 1]


def main() -> None:
    saved_folder = get_date_saved_tracks()
    fingerprints: list[str] = get_config_section("missing").get("fingerprints", [])

    missing_tracks: set[Track] = set()
    for first_date, second_date in grouping_dates(saved_folder):
        first_track, second_track = get_tracks_by_date(first_date), get_tracks_by_date(second_date)

        diff = diff_tracks(first_track, second_track)
        missing_tracks.update(diff.deleted_tracks)

    last_saved_track = set(get_tracks_by_date(saved_folder[-1]))

    print("Пропавшие треки:")
    missing_tracks_count = 0
    for missing_track in missing_tracks - last_saved_track:
        track_info = get_track_info(missing_track)
        if track_info in fingerprints:
            continue

        missing_tracks_count += 1
        print(track_info)

    print("\n")
    print("СТАТИСТИКА:")
    print(f"1. Количество пропавших треков: {missing_tracks_count}")


if __name__ == "__main__":
    main()
