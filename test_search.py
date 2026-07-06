from ytmusicapi import YTMusic
from youtube.search import search_song


def main():

    ytmusic = YTMusic("browser.json")

    results = search_song(
        ytmusic,
        "Hai Re (From \"Itllu Arjuna\")",
        "Thaman S"
    )

    first_song = results[0]

    print("Title :", first_song["title"])

    print(
    "Artist:",
    first_song["artists"][0]["name"]
    )

    print(
    "Video ID:",
    first_song["videoId"]
    )


if __name__ == "__main__":
    main()