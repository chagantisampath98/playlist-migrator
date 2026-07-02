from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from spotify.tracks import get_playlist_tracks


def main():
    print("Connecting to Spotify...\n")

    sp = get_spotify_client()

    user = sp.current_user()

    print(f"Welcome {user['display_name']}!\n")

    playlists = get_user_playlists(sp)

    print("🎵 Your Spotify Playlists\n")

    for index, playlist in enumerate(playlists, start=1):
        print(
            f"{index}. {playlist['name']} ({playlist['tracks']} songs)"
        )

    playlist = playlists[0]

    print(f"\nReading playlist: {playlist['name']}\n")

    songs = get_playlist_tracks(sp, playlist["id"])

    for index, song in enumerate(songs[:20], start=1):
        print(
            f"{index}. {song.title} - {song.artist}"
        )


if __name__ == "__main__":
    main()