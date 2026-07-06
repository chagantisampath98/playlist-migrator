from ytmusicapi import YTMusic

from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from spotify.tracks import get_playlist_tracks

from youtube.matcher import find_song_on_youtube


def main():

    print("Connecting to Spotify...")
    sp = get_spotify_client()

    print("Connecting to YouTube Music...")
    ytmusic = YTMusic("browser.json")

    playlists = get_user_playlists(sp)

    playlist = playlists[0]

    print(f"\nReading playlist: {playlist['name']}\n")

    songs = get_playlist_tracks(sp, playlist["id"])

    print(f"Found {len(songs)} Spotify songs.\n")

    print("Searching first 10 songs on YouTube Music...\n")

    for index, song in enumerate(songs[:10], start=1):

        match = find_song_on_youtube(ytmusic, song)

        if match:
            print(f"{index}. ✅ {song.title}")
            print(f"   YouTube: {match['title']}")
            print(f"   Video ID: {match['videoId']}\n")
        else:
            print(f"{index}. ❌ {song.title}")
            print("   No match found.\n")


if __name__ == "__main__":
    main()