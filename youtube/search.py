def search_song(youtube, title, artist):
    """
    Search YouTube for a song using both title and artist.
    """

    query = f"{title} {artist} official audio"

    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=5
    )

    response = request.execute()

    return response.get("items", [])