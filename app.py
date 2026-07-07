import streamlit as st

from spotify.auth import get_spotify_client
from spotify.playlists import get_user_playlists
from youtube.auth import get_youtube_client
from migration_service import migrate_playlist


st.set_page_config(
    page_title="Playlist Migrator",
    page_icon="🎵"
)

st.title("🎵 Spotify → YouTube Playlist Migrator")
st.write("Migrate your Spotify playlists to YouTube.")

sp = get_spotify_client()
youtube = get_youtube_client()

playlists = get_user_playlists(sp)

playlist_names = [playlist["name"] for playlist in playlists]

selected_name = st.selectbox(
    "Select Spotify Playlist",
    playlist_names
)

selected_playlist = playlists[playlist_names.index(selected_name)]

playlist_name = st.text_input(
    "YouTube Playlist Name",
    value=f"{selected_name} - YouTube"
)

if st.button("Start Migration"):
    with st.spinner("Migrating playlist..."):
        result = migrate_playlist(
            sp,
            youtube,
            selected_playlist,
            playlist_name
        )

    if not result:
        st.error("No songs matched. Playlist was not created.")
    else:
        st.success("Migration Completed!")

        st.metric("Total Songs", result["total"])
        st.metric("Matched Songs", result["matched"])
        st.metric("Added Songs", result["added"])
        st.metric("Failed Songs", result["failed"])

        with open(result["report_file"], "rb") as file:
            st.download_button(
                "Download Report",
                file,
                file_name="migration_report.json"
            )