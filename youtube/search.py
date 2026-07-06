from ytmusicapi import YTMusic


def search_song(ytmusic, title, artist):
    """
    Search for a song on YouTube Music.
    """

    query = f"{title} {artist}"

    results = ytmusic.search(
        query=query,
        filter="songs"
    )

    return results