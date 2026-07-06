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
        print(f"{index}. {playlist['name']} ({playlist['tracks']} songs)")

    print("\n")

    # 🔥 User chooses playlist (FIXED)
    while True:
        try:
            choice = int(input("Enter playlist number: "))

            if choice < 1 or choice > len(playlists):
                print("❌ Number out of range. Try again.\n")
                continue

            break

        except ValueError:
            print("❌ Please enter a valid number.\n")

    selected_playlist = playlists[choice - 1]

    print(f"\nReading playlist: {selected_playlist['name']}\n")

    songs = get_playlist_tracks(sp, selected_playlist["id"])

    for index, song in enumerate(songs[:20], start=1):
        print(f"{index}. {song.title} - {song.artist}")


if __name__ == "__main__":
    main()