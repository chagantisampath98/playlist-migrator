from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from youtube.auth import get_youtube_client
from migration_service import migrate_playlist


def choose_playlist(playlists):
    print("\n🎵 Your Spotify Playlists\n")

    for index, playlist in enumerate(playlists, start=1):
        print(f"{index}. {playlist['name']} ({playlist['tracks']} songs)")

    while True:
        try:
            choice = int(input("\nEnter source playlist number: "))

            if choice < 1 or choice > len(playlists):
                print("❌ Number out of range.")
                continue

            return playlists[choice - 1]

        except ValueError:
            print("❌ Please enter a valid number.")


def main():
    print("Connecting to Spotify...")
    sp = get_spotify_client()

    print("Connecting to YouTube...")
    youtube = get_youtube_client()

    playlists = get_user_playlists(sp)
    source_playlist = choose_playlist(playlists)

    target_playlist_name = input("\nEnter target YouTube playlist name: ")

    result = migrate_playlist(
        sp,
        youtube,
        source_playlist,
        target_playlist_name
    )

    if not result:
        print("No songs matched. Playlist was not created.")
        return

    print("\n" + "=" * 50)
    print("Migration Completed Successfully")
    print("=" * 50)
    print(f"Source Playlist : {source_playlist['name']}")
    print(f"Target Playlist : {target_playlist_name}")
    print(f"Total Songs     : {result['total']}")
    print(f"Matched         : {result['matched']}")
    print(f"Added           : {result['added']}")
    print(f"Failed          : {result['failed']}")
    print(f"Report Saved    : {result['report_file']}")


if __name__ == "__main__":
    main()