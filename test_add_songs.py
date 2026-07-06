from ytmusicapi import YTMusic

from youtube.playlists import create_playlist, add_songs_to_playlist


def main():
    ytmusic = YTMusic("browser.json")

    playlist_id = create_playlist(
        ytmusic,
        "Spotify Migration Test 2"
    )

    video_ids = [
        "5y85R9e5jkY"
    ]

    add_songs_to_playlist(
        ytmusic,
        playlist_id,
        video_ids
    )

    print("Playlist created and song added!")
    print(f"Playlist ID: {playlist_id}")


if __name__ == "__main__":
    main()