import streamlit as st
import pandas as pd
import numpy as np
import whisper

from utils import load_audio, searcher

# Set app wide config
st.set_page_config(
    page_title="Video Search",
    page_icon="🤖",
    menu_items={
        "Get Help": "https://twitter.com/coledrain",
        "Report a bug": "https://github.com/coledrain",
        "About": """This project implements an interface for searching videos.
        Please report any bugs or issues on [Github](https://github.com/coledrain/). Thanks!""",
    },
)

@st.cache
def load_model():
    return whisper.load_model("tiny.en")

# Title
st.title('Search Videos/Audios Easily')

# Upload
uploaded_file = st.file_uploader("Upload a file")

# Text Input
query = st.text_input(
        "Enter some query 👇"
    )

if uploaded_file is not None:
    # To read file as bytes:
    audio_bytes = uploaded_file.getvalue()
    # audio_bytes are the bytes of the audio file
    mel = load_audio(audio_bytes )

    # Search button
    clicked = st.button('Search')

    if len(query) > 1:
        if clicked:
            data_load_state = st.text('Searching...')

            model = load_model()
            trans_dict = model.transcribe(mel, language='english')

            search_result = searcher(trans_dict, query)

            data_load_state.text('Search.. done!')

            st.write(search_result)


# def seeker(start_timestamp: str):
#     st.audio(audio_bytes, start_time)

# def display_stamps(search_result):
#     col1, col2, col3 = st.columns(3)
