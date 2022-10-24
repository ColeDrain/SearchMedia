from pytube import YouTube
import streamlit as st
import os

@st.experimental_memo
def get_yt_bytes(yt_link):
    audio = YouTube(yt_link).streams.filter(only_audio=True).first().download()
    with open(audio, "rb") as f:
        _bytes = f.read()
        os.remove(audio)
        return _bytes