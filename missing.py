from functools import cache
from typing import Iterator

from yandex_music import Track

from common import TrackType, get_date_saved_tracks
from diff import diff_tracks, track_info


@cache
def get_tracks_by_date(date: str) -> list[Track]:
    """В обычной ситуации такой кейс не нужен. Сделано из-за повторного получения треков"""
    import common

    return common.get_tracks_by_date(TrackType.LIKES, date)


def grouping_dates(saved_folder: list[str]) -> Iterator[tuple[str, str]]:
    for idx, el in enumerate(saved_folder[:-1]):
        yield el, saved_folder[idx + 1]


def main() -> None:
    saved_folder = get_date_saved_tracks()

    missing_tracks: set[Track] = set()
    for first_date, second_date in grouping_dates(saved_folder):
        first_track, second_track = get_tracks_by_date(first_date), get_tracks_by_date(second_date)

        diff = diff_tracks(first_track, second_track)
        missing_tracks.update(diff.deleted_tracks)

    last_saved_track = set(get_tracks_by_date(saved_folder[-1]))

    print("Пропавшие треки:")
    for missing_track in missing_tracks - last_saved_track:
        print(track_info(missing_track))


if __name__ == "__main__":
    main()
