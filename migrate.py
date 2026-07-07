from tqdm import tqdm

from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from spotify.tracks import get_playlist_tracks

from youtube.search import search_song
from youtube.auth import get_youtube_client
from youtube.playlists import create_playlist, add_video_to_playlist

from utils.matcher import find_best_match
from utils.report import save_report


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

    print("Connecting to official YouTube API...")
    youtube = get_youtube_client()

    playlists = get_user_playlists(sp)
    source_playlist = choose_playlist(playlists)

    target_playlist_name = input("\nEnter target YouTube playlist name: ")

    songs = get_playlist_tracks(sp, source_playlist["id"])
    total = len(songs)

    video_ids = []
    matched_songs = []
    failed_songs = []

    for index, song in enumerate(
        tqdm(songs, desc="Searching Songs", unit="song"),
        start=1
    ):
        print(f"[{index}/{total}] Searching: {song.title}")

        results = search_song(youtube, song.title, song.artist)
        match = find_best_match(results, song)

        if match:
            video_id = match["id"]["videoId"]
            video_ids.append(video_id)

            matched_songs.append({
                "spotify": song.title,
                "artist": song.artist,
                "youtube": match["snippet"]["title"],
                "videoId": video_id,
            })

            print(f"✅ Found: {match['snippet']['title']}\n")

        else:
            failed_songs.append({
                "spotify": song.title,
                "artist": song.artist,
            })

            print(f"❌ No match: {song.title}\n")

    if not video_ids:
        print("No songs matched. Playlist was not created.")
        return

    playlist_id = create_playlist(
        youtube,
        target_playlist_name,
        f"Migrated from Spotify playlist: {source_playlist['name']}"
    )

    print("\nCreated YouTube playlist.")

    added_count = 0

    for index, video_id in enumerate(video_ids, start=1):
        print(f"Adding song {index}/{len(video_ids)}")

        success = add_video_to_playlist(youtube, playlist_id, video_id)

        if success:
            added_count += 1

    report_file = save_report(
        source_playlist["name"],
        target_playlist_name,
        matched_songs,
        failed_songs
    )

    print("\n" + "=" * 50)
    print("Migration Completed Successfully")
    print("=" * 50)

    print(f"Source Playlist : {source_playlist['name']}")
    print(f"Target Playlist : {target_playlist_name}")
    print(f"Total Songs     : {total}")
    print(f"Matched         : {len(matched_songs)}")
    print(f"Added           : {added_count}")
    print(f"Failed          : {len(failed_songs)}")
    print(f"Report Saved    : {report_file}")


if __name__ == "__main__":
    main()