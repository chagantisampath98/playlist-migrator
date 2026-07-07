from tqdm import tqdm

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

    for song in tqdm(songs, desc="Searching Songs", unit="song"):
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
                    "reason": "No match found",
                })

        except Exception as error:
            failed_songs.append({
                "spotify": song.title,
                "artist": song.artist,
                "reason": str(error),
            })
            logger.error(f"Search failed for {song.title}: {error}")

    if not matched_songs:
        return None

    playlist_id = create_playlist(
        youtube,
        target_playlist_name,
        f"Migrated from Spotify playlist: {source_playlist['name']}"
    )

    added_count = 0

    for song in matched_songs:
        success = add_video_to_playlist(
            youtube,
            playlist_id,
            song["videoId"]
        )

        if success:
            added_count += 1

    report_file = save_report(
        source_playlist["name"],
        target_playlist_name,
        matched_songs,
        failed_songs
    )

    return {
        "playlist_id": playlist_id,
        "total": total,
        "matched": len(matched_songs),
        "added": added_count,
        "failed": len(failed_songs),
        "report_file": report_file,
    }