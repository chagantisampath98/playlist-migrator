from ytmusicapi import YTMusic

from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from spotify.tracks import get_playlist_tracks

from youtube.matcher import find_song_on_youtube
from youtube.playlists import create_playlist, add_songs_to_playlist


def choose_playlist(playlists):
    print("\n🎵 Your Spotify Playlists\n")

    for index, playlist in enumerate(playlists, start=1):
        print(f"{index}. {playlist['name']} ({playlist['tracks']} songs)")

    while True:
        try:
            choice = int(input("\nEnter source playlist number: "))

            if choice < 1 or choice > len(playlists):
                print("❌ Number out of range. Try again.")
                continue

            return playlists[choice - 1]

        except ValueError:
            print("❌ Please enter a valid number.")


def main():
    print("Connecting to Spotify...")
    sp = get_spotify_client()

    print("Connecting to YouTube Music...")
    ytmusic = YTMusic("browser.json")

    playlists = get_user_playlists(sp)

    source_playlist = choose_playlist(playlists)

    target_playlist_name = input(
        "\nEnter target YouTube Music playlist name: "
    )

    print(f"\nMigrating: {source_playlist['name']}")
    print(f"Target playlist: {target_playlist_name}\n")

    songs = get_playlist_tracks(sp, source_playlist["id"])
    total = len(songs)

    print(f"Found {total} songs.\n")

    video_ids = []

    for index, song in enumerate(songs, start=1):
        print(f"[{index}/{total}] Searching: {song.title}")

        match = find_song_on_youtube(ytmusic, song)

        if match and "videoId" in match:
            video_ids.append(match["videoId"])
            print(f"✅ Found: {match['title']}\n")
        else:
            print(f"❌ No match: {song.title}\n")

    playlist_id = create_playlist(
        ytmusic,
        target_playlist_name
    )

    print("\nCreated YouTube Music playlist!")

    add_songs_to_playlist(
        ytmusic,
        playlist_id,
        video_ids
    )

    print("\nMigration Complete!")
    print(f"Matched songs: {len(video_ids)}")
    print(f"Failed songs: {total - len(video_ids)}")


if __name__ == "__main__":
    main()