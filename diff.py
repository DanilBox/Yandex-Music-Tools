from typing import NamedTuple

from yandex_music import Track

from base_client import null_client
from common import get_parent_save_date, get_tracks_by_date


class DiffResult(NamedTuple):
    added_tracks: list[Track]
    deleted_tracks: list[Track]

    def empty(self) -> bool:
        return len(self.added_tracks) == 0 and len(self.deleted_tracks) == 0


def diff_tracks(tracks_from: list[Track], tracks_to: list[Track]) -> DiffResult:
    return DiffResult(
        added_tracks=list(set(tracks_to) - set(tracks_from)),
        deleted_tracks=list(set(tracks_from) - set(tracks_to)),
    )


def diff_object(object_type: str) -> DiffResult:
    this_track = get_tracks_by_date(object_type)
    parent_track = get_tracks_by_date(object_type, get_parent_save_date())

    return diff_tracks(parent_track, this_track)


def track_info(track: Track) -> str:
    artists = ", ".join(sorted([artist.name for artist in track.artists]))
    return f"'{track.title}' by '{artists}' ({track.track_id})"


def show_diff(result: DiffResult) -> None:
    print("Новые добавленные треки:")
    for new_track in result.added_tracks:
        print(track_info(new_track))

    print()

    print("Удалённые треки:")
    for del_track in result.deleted_tracks:
        print(track_info(del_track))

    print()


def show_diff_object(object_type: str) -> None:
    result = diff_object(object_type)

    if not result.empty():
        print(f"Разница по объекту {object_type}")
        show_diff(result)


def main() -> None:
    _ = null_client()

    show_diff_object("likes")
    show_diff_object("dislikes")


if __name__ == "__main__":
    main()
