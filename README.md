# 🎙️ VoiceScribe AI

A professional multilingual Speech-to-Text web application built using **Streamlit**, **Google Gemini AI**, and **SQLite**.

The application converts speech into text, stores transcripts in a database, and provides complete transcript management with a modern UI.

---

## 🚀 Features

- 🎤 Speech to Text using Google Gemini AI
- 🌍 Multilingual Transcription
  - English
  - Hindi
  - Marathi
  - Hinglish
- 💾 Save transcripts to SQLite Database
- 📜 Transcript History
- 🔍 Search transcripts
- ✏️ Edit transcripts
- 🗑️ Delete transcripts
- 📄 Download as TXT
- 📑 Download as PDF
- 📊 Dashboard Statistics
- 🎨 Professional Streamlit UI

---

## 🛠 Tech Stack

- Python 3.12
- Streamlit
- Google Gemini API
- SQLite
- ReportLab
- gTTS
- streamlit-webrtc
- audio-recorder-streamlit

---

## 📂 Project Structure

```text
speech_to_text_app/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── database/
│   ├── db.py
│   ├── models.py
│
├── services/
│   ├── audio_recorder.py
│   ├── gemini_service.py
│   └── text_to_speech.py
│
├── pages/
│   └── 1_History.py
│
└── .streamlit/
    └── config.toml
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/VoiceScribe-AI.git
```

Go inside project

```bash
cd VoiceScribe-AI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Create `.env`

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run project

```bash
streamlit run app.py
```

---

## 📸 Screenshots

### Home

(Add Screenshot)

### Transcript History

(Add Screenshot)

---

## 🎯 Assignment Requirements Covered

- ✅ Speech To Text
- ✅ Multilingual Speech
- ✅ Database Storage
- ✅ Transcript History
- ✅ CRUD Operations
- ✅ Professional UI
- ✅ PDF Export
- ✅ TXT Export

---

## 🔮 Future Improvements

- Gemini Live API
- Real-time Streaming
- Speaker Identification
- Audio File Upload
- Translation Support
- Cloud Database
- User Authentication

---

## 👨‍💻 Developer

**Prashant Kadu**

AI / ML Engineer

---

## 📄 License

MIT License