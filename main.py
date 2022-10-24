import streamlit as st

from utils import load_audio, searcher, load_model, transcribe, col_displayer
from youtube_handler import get_yt_bytes

# Set app wide config
st.set_page_config(
    page_title="Video Search",
    page_icon="🤖",
    menu_items={
        "Get Help": "https://twitter.com/coledrain",
        "Report a bug": "https://github.com/coledrain",
        "About": """This project implements an interface for searching videos using Open AI [Whisper](https://github.com/openai/whisper) Models.
        Please report any bugs or issues on [Github](https://github.com/coledrain/). Thanks!""",
    },
)

model = load_model()

audio_ext = ["mp3", "ogg", "wav", "aac", "m4a", "flac", "avi", "wma"]
video_ext = ["mp4", "mkv", "mov", "wmv"]

reduce_header_height_style = """
    <style>
        div.block-container {padding-top:1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

# Title
st.title('Search Videos/Audios Easily')

# Brand
'Made by [Ugochukwu Onyebuchi](https://linkedin.com/in/ugochukwu-onyebuchi) 🤖'

upload_type = st.radio(
    "What kind of video do you wanna search ?",
    ('YouTube Vid', 'Local Video'))


if upload_type == 'YouTube Vid':
    yt_link = st.text_input("Enter a YouTube Video Link")
    if len(yt_link) > 10:
        audio_bytes = get_yt_bytes(yt_link)

        # Text Input
        query = st.text_input("Enter some query 👇")

        # audio_bytes are the bytes of the audio file
        audio_array = load_audio(audio_bytes)

        clicked = st.button('Search')

        # Search button
        if clicked:
            if len(query) > 1:
                data_load_state = st.text('Searching...')

                trans_dict = transcribe(model, audio_array)

                search_result = searcher(trans_dict, query)

                data_load_state.text('Search.. done!')

                if search_result:
                    st.write(f"we found '{query}' at the following position(s):")

                    st.write(", ".join(search_result))
                else:
                    st.write(f"we couldn't find '{query}' ")

else:
    # Upload
    uploaded_file = st.file_uploader("Upload a file", type=audio_ext+video_ext)
    if uploaded_file is not None:
        # To read file as bytes:
        audio_bytes = uploaded_file.getvalue()

        # Text Input
        query = st.text_input("Enter some query 👇")

        # audio_bytes are the bytes of the audio file
        audio_array = load_audio(audio_bytes)

        clicked = st.button('Search')

        # Search button
        if clicked:
            if len(query) > 1:
                data_load_state = st.text('Searching...')

                trans_dict = transcribe(model, audio_array)

                search_result = searcher(trans_dict, query)

                data_load_state.text('Search.. done!')

                if search_result:
                    st.write(f"we found '{query}' at the following position(s):")

                    st.write(", ".join(search_result))
                else:
                    st.write(f"we couldn't find {query}")


# def seeker(start_timestamp: str):
#     st.audio(audio_bytes, start_time)
