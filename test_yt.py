from ytmusicapi import YTMusic

yt = YTMusic("browser.json")

playlists = yt.get_library_playlists()

for playlist in playlists:
    print(playlist["title"])