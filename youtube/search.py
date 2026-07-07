def search_song(youtube, title, artist):
    query = f"{title} {artist} official song"

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5
    )

    response = request.execute()
    return response.get("items", [])