from youtube.search import search_song


def find_song_on_youtube(ytmusic, song):
    """
    Search a Spotify song on YouTube Music.
    Returns the first matching result.
    """

    results = search_song(
        ytmusic,
        song.title,
        song.artist
    )

    if not results:
        return None

    return results[0]