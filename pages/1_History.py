import streamlit as st
from database.models import (
    get_all_transcripts, 
    delete_transcript, 
    search_transcripts,
    update_transcript
)
from database.db import create_table
from services.export_service import (
    create_txt,
    create_pdf
)
# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="VoiceScribe | History",
    page_icon="📜",
    layout="wide"
)

create_table()

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
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    .history-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .history-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .transcript-id {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .transcript-date {
        color: #888;
        font-size: 0.85rem;
    }
    
    .transcript-text {
        margin-top: 0.8rem;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        color: #2c3e50;
        line-height: 1.6;
    }
    
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #95a5a6;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .stats-bar {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .stat-pill {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        color: #1a1a2e;
        border-left: 3px solid #667eea;
    }
    
    .divider-custom {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
    }
    
    .lang-flag {
        font-size: 1.2rem;
        margin-right: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown('<div style="font-size: 1.2rem; font-weight: 600; color: #1a1a2e; padding-bottom: 0.5rem; border-bottom: 2px solid #667eea; margin-bottom: 1rem;">🗂️ Navigation</div>', unsafe_allow_html=True)
    
    #st.page_link("test.py", label="🏠 Home", icon="🏠")
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_History.py", label="📜 Transcript History", icon="📜")
    
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
        <h1>📜 Transcript History</h1>
        <p>View, search, edit and manage all your speech-to-text records</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SEARCH & STATS ---------------- #
transcripts = get_all_transcripts(limit=100)

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "🔍 Search transcripts...", 
        placeholder="Type keywords to search...",
        label_visibility="collapsed"
    )

with col2:
    sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First"])

# Stats
st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-pill">📊 Total: {len(transcripts)}</div>
    </div>
""", unsafe_allow_html=True)

# Filter transcripts
if search_query:
    filtered_transcripts = search_transcripts(search_query)
    st.info(f"🔍 Found **{len(filtered_transcripts)}** results for '{search_query}'")
else:
    filtered_transcripts = transcripts

if sort_order == "Oldest First":
    filtered_transcripts = list(reversed(filtered_transcripts))

# Language display map
lang_flags = {
    "auto": "🌍", "en": "🇺🇸", "hi": "🇮🇳", "hi-en": "🇮🇳",
    "mr": "🇮🇳", "es": "🇪🇸", "fr": "🇫🇷"
}

# ---------------- TRANSCRIPTS LIST ---------------- #
if not filtered_transcripts:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h3>No Transcripts Found</h3>
            <p>Start recording on the Home page to see your transcripts here.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for transcript in filtered_transcripts:
        flag = lang_flags.get(transcript.get('language', 'auto'), '🌍')
        
        with st.container():
            st.markdown(f"""
                <div class="history-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span class="transcript-id">#{transcript['id']}</span>
                        <div>
                            <span style="margin-right: 0.5rem;">{flag}</span>
                            <span class="transcript-date">🕐 {transcript['created_at']}</span>
                        </div>
                    </div>
                    <div class="transcript-text">
                        {transcript['text'][:300]}{'...' if len(transcript['text']) > 300 else ''}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 3])
            
            with btn_col1:
                if st.button("📋 Copy", key=f"copy_{transcript['id']}", use_container_width=True):
                    st.code(transcript['text'])
                    st.toast("📋 Copied!", icon="📋")
            
            with btn_col2:
                if st.button("✏️ Edit", key=f"edit_{transcript['id']}", use_container_width=True):
                    st.session_state[f"editing_{transcript['id']}"] = True
            
            with btn_col3:
                if st.button("🗑️ Delete", key=f"del_{transcript['id']}", use_container_width=True):
                    if delete_transcript(transcript['id']):
                        st.toast("🗑️ Deleted successfully!", icon="🗑️")
                        st.rerun()
                    else:
                        st.error("Failed to delete")

            download_col1, download_col2 = st.columns(2)
            with download_col1:

                st.download_button(

                    "📄 TXT",

                    data=create_txt(transcript["text"]),

                    file_name=f"transcript_{transcript['id']}.txt",

                    mime="text/plain",

                    use_container_width=True
                )

            with download_col2:

                st.download_button(

                    "📕 PDF",

                    data=create_pdf(transcript["text"]),

                    file_name=f"transcript_{transcript['id']}.pdf",

                    mime="application/pdf",

                    use_container_width=True
                )
            
            # Edit expander
            if st.session_state.get(f"editing_{transcript['id']}", False):
                with st.expander("✏️ Edit Transcript", expanded=True):
                    new_text = st.text_area(
                        "Edit text",
                        value=transcript['text'],
                        height=150,
                        key=f"text_{transcript['id']}"
                    )
                    save_col, cancel_col = st.columns([1, 3])
                    with save_col:
                        if st.button("💾 Update", key=f"save_{transcript['id']}", type="primary"):
                            if update_transcript(transcript['id'], new_text):
                                st.toast("✅ Updated!", icon="✅")
                                del st.session_state[f"editing_{transcript['id']}"]
                                st.rerun()
                    with cancel_col:
                        if st.button("❌ Cancel", key=f"cancel_{transcript['id']}"):
                            del st.session_state[f"editing_{transcript['id']}"]
                            st.rerun()
            
            # Full view expander
            with st.expander("👁️ View Full Transcript"):
                st.write(transcript['text'])
            
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.3;'>", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #
st.markdown('<div class="divider-custom"></div>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎙️ VoiceScribe | Built with Streamlit & Gemini AI</p>
        <p style="font-size: 0.8rem;">© 2024 | Secure & Private Transcription</p>
    </div>
""", unsafe_allow_html=True)