from spotify.tracks import get_playlist_tracks
from youtube.playlists import create_playlist, add_video_to_playlist
from youtube.search import search_song
from utils.matcher import find_best_match
from utils.report import save_report
from utils.logger import logger


def migrate_playlist(sp, youtube, source_playlist, target_playlist_name):
    songs = get_playlist_tracks(sp, source_playlist["id"])
    total = len(songs)

    matched_songs = []
    failed_songs = []

    print(f"Searching {total} songs...")

    for index, song in enumerate(songs, start=1):
        print(f"[{index}/{total}] Searching: {song.title}")

        try:
            results = search_song(youtube, song.title, song.artist)
            match = find_best_match(results, song)

            if match:
                matched_songs.append({
                    "spotify": song.title,
                    "artist": song.artist,
                    "youtube": match["snippet"]["title"],
                    "videoId": match["id"]["videoId"],
                })
            else:
                failed_songs.append({
                    "spotify": song.title,
                    "artist": song.artist,
                    "error": "No match found",
                })

        except Exception as error:
            error_text = str(error)

            if "Quota exceeded" in error_text:
                return {
                    "quota_exceeded": True,
                    "message": "YouTube API quota exceeded. Try again tomorrow.",
                }

            failed_songs.append({
                "spotify": song.title,
                "artist": song.artist,
                "error": error_text,
            })

            logger.error(f"Search failed for {song.title}: {error_text}")

    if not matched_songs:
        return None

    playlist_id = create_playlist(
        youtube,
        target_playlist_name,
        f"Migrated from Spotify playlist: {source_playlist['name']}",
    )

    added_count = 0

    for index, song in enumerate(matched_songs, start=1):
        print(f"Adding {index}/{len(matched_songs)}")

        success = add_video_to_playlist(
            youtube,
            playlist_id,
            song["videoId"],
        )

        if success:
            added_count += 1

    report_file = save_report(
        source_playlist["name"],
        target_playlist_name,
        matched_songs,
        failed_songs,
    )

    return {
        "playlist_id": playlist_id,
        "total": total,
        "matched": len(matched_songs),
        "added": added_count,
        "failed": len(failed_songs),
        "report_file": report_file,
    }