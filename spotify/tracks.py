from models.song import Song


def get_playlist_tracks(sp, playlist_id):
    songs = []
    results = sp.playlist_items(playlist_id)

    while True:
        for item in results["items"]:
            track = item.get("track") or item.get("item")

            if not track:
                continue

            songs.append(
                Song(
                    title=track["name"],
                    artist=", ".join(
                        artist["name"] for artist in track["artists"]
                    ),
                    album=track["album"]["name"],
                    duration_ms=track["duration_ms"],
                    spotify_id=track["id"],
                )
            )

        if results.get("next"):
            results = sp.next(results)
        else:
            break

    return songs