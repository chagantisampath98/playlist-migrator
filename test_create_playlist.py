from ytmusicapi import YTMusic

from youtube.playlists import create_playlist


def main():

    ytmusic = YTMusic("browser.json")

    playlist_name = input("Enter new playlist name: ")

    playlist_id = create_playlist(
        ytmusic,
        playlist_name
    )

    print("Playlist created successfully!")
    print(f"Playlist ID: {playlist_id}")


if __name__ == "__main__":
    main()