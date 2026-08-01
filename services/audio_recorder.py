import streamlit as st
from audio_recorder_streamlit import audio_recorder


def record_audio():
    audio_bytes = audio_recorder(
        text="Click to record",
        recording_color="#e74c3c",
        neutral_color="#667eea",
        icon_name="microphone",
        icon_size="3x",
    )
    if audio_bytes:
        return {"bytes": audio_bytes}
    return None