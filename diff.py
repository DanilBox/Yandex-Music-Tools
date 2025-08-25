from collections.abc import Sequence
from typing import NamedTuple

from yandex_music import Artist, Track

from base_client import null_client
from common import TrackType, get_parent_save_date, get_tracks_by_date


class DiffResult(NamedTuple):
    added_tracks: list[Track]
    deleted_tracks: list[Track]

    def empty(self) -> bool:
        return len(self.added_tracks) == 0 and len(self.deleted_tracks) == 0

    def get_added_tracks(self) -> list[Track]:
        return sort_track_list(self.added_tracks)

    def get_deleted_tracks(self) -> list[Track]:
        return sort_track_list(self.deleted_tracks)


def show_artist(artists: list[Artist]) -> str:
    return ", ".join(sorted([artist.name for artist in artists]))


def sort_track_list(track: list[Track]) -> list[Track]:
    def sort_tract(_track: Track) -> str:
        return show_artist(_track.artists)

    return sorted(track, key=sort_tract, reverse=True)


def diff_tracks(tracks_from: Sequence[Track], tracks_to: Sequence[Track]) -> DiffResult:
    return DiffResult(
        added_tracks=list(set(tracks_to) - set(tracks_from)),
        deleted_tracks=list(set(tracks_from) - set(tracks_to)),
    )


def diff_object(object_type: str) -> DiffResult:
    this_track = get_tracks_by_date(object_type)
    parent_track = get_tracks_by_date(object_type, get_parent_save_date())

    return diff_tracks(parent_track, this_track)


def get_track_info(track: Track) -> str:
    return f"'{track.title}' by '{show_artist(track.artists)}' ({track.track_id})"


def show_diff(result: DiffResult) -> None:
    print("Новые добавленные треки:")
    for new_track in result.get_added_tracks():
        print(get_track_info(new_track))

    print()

    print("Удалённые треки:")
    for del_track in result.get_deleted_tracks():
        print(get_track_info(del_track))

    print()


def show_diff_object(object_type: str) -> None:
    result = diff_object(object_type)

    if not result.empty():
        print(f"Разница по объекту {object_type}")
        show_diff(result)


def main() -> None:
    _ = null_client()

    show_diff_object(TrackType.LIKES)
    show_diff_object(TrackType.DISLIKES)


if __name__ == "__main__":
    main()
