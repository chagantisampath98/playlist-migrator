import time

from googleapiclient.errors import HttpError


def create_playlist(youtube, title, description):
    response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": "private",
            },
        },
    ).execute()

    return response["id"]


def add_video_to_playlist(youtube, playlist_id, video_id):
    for attempt in range(3):
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                },
            ).execute()

            return True

        except HttpError as error:
            print(f"Retry {attempt + 1}/3 failed: {error}")
            time.sleep(2)

    return False