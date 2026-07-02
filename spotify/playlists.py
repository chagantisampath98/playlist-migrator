def get_user_playlists(sp):
    playlists = []

    results = sp.current_user_playlists()

    while True:
        for item in results["items"]:
            playlists.append({
                "id": item["id"],
                "name": item["name"],
                "tracks": item.get("items", {}).get("total", 0)
            })

        if results.get("next"):
            results = sp.next(results)
        else:
            break

    return playlists