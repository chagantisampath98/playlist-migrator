def search_song(youtube, title, artist):
    query = f"{title} {artist} official song"

    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5,
    ).execute()

    return response.get("items", [])