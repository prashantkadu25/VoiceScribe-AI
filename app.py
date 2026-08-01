import streamlit as st
from services.audio_recorder import record_audio
#from services.live_audio import start_live_audio
from services.gemini_service import speech_to_text
from services.tts_service import text_to_speech
from database.db import create_table
from database.models import (
    save_transcript,
    get_todays_transcripts
)
from database.models import (
    get_total_transcripts,
    get_today_records,
    get_total_words,
    get_total_characters
)
from services.live_transcriber import get_latest
import os

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }
    
    .transcript-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e9ecef;
        min-height: 200px;
        font-size: 1rem;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #95a5a6;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .divider-custom {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
    }
    
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a2e;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .lang-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #667eea;
        color: white;
        margin-left: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="VoiceScribe | Real-Time Speech To Text",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()

live_text = get_latest()

if live_text:
    st.session_state.transcript += " " + live_text
# Session State
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "audio_processed" not in st.session_state:
    st.session_state.audio_processed = False

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown('<div class="sidebar-header">🗂️ Navigation</div>', unsafe_allow_html=True)
    
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_History.py", label="📜 Transcript History", icon="📜")
    
    st.markdown("---")
    st.markdown('<div class="sidebar-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    language = st.selectbox(
        "🌐 Transcription Language",
        [
            "Auto-Detect (Multilingual)",
            "English (US)",
            "Hindi",
            "Hindi + English (Hinglish)",
            "Marathi",
            "Spanish",
            "French"
        ],
        index=0,
        help="Select the language of your speech. Choose 'Hindi + English' for mixed language."
    )
    
    # Map selection to API hint
    lang_map = {
        "Auto-Detect (Multilingual)": "auto",
        "English (US)": "en",
        "Hindi": "hi",
        "Hindi + English (Hinglish)": "hi-en",
        "Marathi": "mr",
        "Spanish": "es",
        "French": "fr"
    }
    
    auto_save = st.toggle("💾 Auto-save Transcripts", value=False, help="Automatically save transcripts after generation")
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>🎙️ VoiceScribe v1.0</p>
            <p>Powered by Gemini AI</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown("""
    <div class="main-header">
        <h1>🎙️ VoiceScribe</h1>
        <p>Real-Time Multilingual Speech to Text Transcription powered by Gemini AI</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- MAIN LAYOUT ---------------- #
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Recorder Section
    st.subheader("🎤 Speech Recorder")
    
    recorder_col1, recorder_col2 = st.columns([1, 3])
    with recorder_col1:
        st.markdown("""
            <div style="font-size: 3rem; text-align: center; margin-top: 1rem;">
                🎙️
            </div>
        """, unsafe_allow_html=True)
    
    with recorder_col2:
        st.info("Click the microphone below and start speaking clearly.")
        st.caption("💡 Supports Hindi-English mixed speech (Hinglish)")
    
    # Audio Recording (Live)

    audio = record_audio()

    if audio:
        st.audio(audio["bytes"], format="audio/wav")

        transcript = speech_to_text(
            audio["bytes"],
            language_hint=lang_map[language]
        )
    
    # Transcript Display
    st.markdown("---")
    st.subheader("📝 Transcript")
    
    if st.session_state.transcript:
        lang_display = {
            "auto": "🌍 Auto", "en": "🇺🇸 EN", "hi": "🇮🇳 HI", 
            "hi-en": "🇮🇳 HI+EN", "mr": "🇮🇳 MR", "es": "🇪🇸 ES", "fr": "🇫🇷 FR"
        }
        badge = lang_display.get(lang_map[language], "🌍 Auto")
        
        st.markdown(f"""
            <div class="transcript-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600; color: #667eea;">Generated Text</span>
                    <span class="lang-badge">{badge}</span>
                </div>
                {st.session_state.transcript}
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        with btn_col1:
            if st.button("💾 Save", use_container_width=True, type="primary"):
                if st.session_state.transcript.strip():
                    save_transcript(
                        st.session_state.transcript,
                        language=lang_map[language]
                    )
                    st.toast("✅ Saved successfully!", icon="💾")
                    st.session_state.transcript = ""
                    st.session_state.audio_processed = False
                    st.rerun()
                else:
                    st.toast("⚠️ Nothing to save!", icon="⚠️")
        
        with btn_col2:
            if st.button("📋 Copy", use_container_width=True):
                st.text_area(
                    "Transcript",
                    value=st.session_state.transcript,
                    height=220
                )
                st.toast("📋 Copied!", icon="📋")
        
        with btn_col3:
            if st.button("🔊 Speak", use_container_width=True):
                with st.spinner("Generating audio..."):
                    tts_file = text_to_speech(
                        st.session_state.transcript,
                        lang=lang_map[language] if lang_map[language] != "hi-en" else "hi"
                    )
                    if tts_file:
                        st.audio(tts_file, format="audio/mp3")
                        os.remove(tts_file)
        
        with btn_col4:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.transcript = ""
                st.session_state.audio_processed = False
                st.toast("🗑️ Cleared!", icon="🗑️")
                st.rerun()
    else:
        st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📝</div>
                <p><strong>Your transcript will appear here</strong></p>
                <p style="font-size: 0.85rem;">Record audio to get started</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Statistics Cards
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Dashboard")
    
    total = get_total_transcripts()
    today = get_todays_transcripts()
    
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Transcripts</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
            <div class="metric-card" style="border-left-color: #e74c3c;">
                <div class="metric-value">{today}</div>
                <div class="metric-label">Today's Records</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    metric_col3, metric_col4 = st.columns(2)
    with metric_col3:
        st.markdown("""
            <div class="metric-card" style="border-left-color: #27ae60;">
                <div class="metric-value">7+</div>
                <div class="metric-label">Languages</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown("""
            <div class="metric-card" style="border-left-color: #f39c12;">
                <div class="metric-value">95%</div>
                <div class="metric-label">AI Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features
    st.markdown('<div class="card" style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.subheader("✨ Features")
    st.markdown("""
        - 🎤 **Real-time Recording** - One-click audio capture
        - 🌐 **Multilingual** - Hindi, English, Hinglish & more
        - 🤖 **Gemini AI** - Powered by Google's latest model
        - 💾 **Auto-save** - Optional automatic storage
        - 🔊 **Text-to-Speech** - Listen to your transcripts
        - 📱 **Mobile Friendly** - Works on all devices
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Tips
    st.markdown('<div class="card" style="margin-top: 1rem; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);">', unsafe_allow_html=True)
    st.subheader("💡 Pro Tips")
    st.markdown("""
        - 🎤 Keep microphone 6-8 inches away
        - 🔇 Minimize background noise
        - 🐢 Speak clearly and steadily
        - 🇮🇳 Try "Hindi + English" for Hinglish
        - 📶 Ensure stable internet connection
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎙️ VoiceScribe | Built with Streamlit & Gemini AI</p>
        <p style="font-size: 0.8rem;">© 2024 | Secure & Private Transcription</p>
    </div>
""", unsafe_allow_html=True)