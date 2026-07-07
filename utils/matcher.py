def find_best_match(results, song):
    if not results:
        return None

    spotify_title = song.title.lower()

    for result in results:
        youtube_title = result["snippet"]["title"].lower()

        if spotify_title.split("(")[0].strip() in youtube_title:
            return result

    return results[0]