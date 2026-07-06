def create_playlist(ytmusic, title, description="Migrated from Spotify"):
    result = ytmusic.create_playlist(
        title=title,
        description=description,
        privacy_status="PRIVATE"
    )

    print("Create playlist result:", result)

    if isinstance(result, str):
        return result

    if isinstance(result, dict):
        if "playlistId" in result:
            return result["playlistId"]
        if "id" in result:
            return result["id"]

    raise Exception("YouTube Music did not return a playlist ID.")


def add_songs_to_playlist(ytmusic, playlist_id, video_ids):
    ytmusic.add_playlist_items(playlist_id, video_ids)