def find_best_match(results, song):
    if not results:
        return None

    clean_title = song.title.lower().split("(")[0].strip()

    for result in results:
        youtube_title = result["snippet"]["title"].lower()

        if clean_title in youtube_title:
            return result

    return results[0]