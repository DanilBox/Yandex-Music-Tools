from collections import Counter

from common import TrackType, get_tracks_by_date


def main() -> None:
    tracks = get_tracks_by_date(TrackType.LIKES)

    artists_counter: Counter[tuple[str, int]] = Counter()
    for track in tracks:
        for artist in track.artists:
            artists_counter.update([(artist.name, artist.id)])

    print(f"Статистика по {artists_counter.total()} авторам:")
    for artist, count in artists_counter.most_common():
        print(f"{artist[0]} - {count}")


if __name__ == "__main__":
    main()
