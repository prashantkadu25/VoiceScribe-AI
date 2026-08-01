from gtts import gTTS
import tempfile
import streamlit as st
import os


def text_to_speech(text, lang='en'):
    """Convert text to speech using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.error(f"TTS Error: {e}")
        return None