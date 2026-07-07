def find_best_match(results, song):
    """
    Return the first search result whose title contains
    the Spotify song title.
    """

    spotify_title = song.title.lower()

    for result in results:
        youtube_title = result["snippet"]["title"].lower()

        if spotify_title in youtube_title:
            return result

    return results[0] if results else None