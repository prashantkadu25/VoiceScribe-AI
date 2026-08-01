import streamlit as st

from services.live_audio import start_live_audio

st.title("Live Mic Test")

q = start_live_audio()

if not q.empty():

    st.success("Receiving Audio Frames ✅")