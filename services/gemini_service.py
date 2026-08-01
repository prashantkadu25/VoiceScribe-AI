import os
import tempfile
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize client with new google-genai package
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def speech_to_text(audio_bytes, language_hint="auto"):
    """
    Transcribe audio using Gemini 1.5 Flash.
    Supports multilingual transcription (Hindi + English mix).
    """
    try:
        # Write bytes to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        # Upload audio file using new API
        audio_file = client.files.upload(
            file=tmp_path,
            config={"mime_type": "audio/wav"}
        )
        
        # Build prompt based on language
        if language_hint == "hi-en":
            lang_instruction = "Transcribe this audio. The speaker may mix Hindi and English (Hinglish). Preserve the exact words spoken in their original language. Do not translate."
        elif language_hint == "hi":
            lang_instruction = "Transcribe this audio in Hindi language."
        elif language_hint == "en":
            lang_instruction = "Transcribe this audio in English."
        elif language_hint == "mr":
            lang_instruction = "Transcribe this audio in Marathi language."
        elif language_hint == "es":
            lang_instruction = "Transcribe this audio in Spanish."
        elif language_hint == "fr":
            lang_instruction = "Transcribe this audio in French."
        else:
            lang_instruction = "Transcribe this audio accurately. If the speaker uses multiple languages (like Hindi and English mixed), preserve each word in its original spoken language. Do not translate."
        
        prompt = f"""{lang_instruction}
        
        Provide ONLY the transcription text. No explanations, no formatting, just the spoken words as they were spoken."""
        
        # Generate content using new API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[audio_file, prompt]
        )
        
        # Cleanup temp file
        os.unlink(tmp_path)
        
        # Delete uploaded file from Gemini (optional cleanup)
        try:
            client.files.delete(name=audio_file.name)
        except:
            pass
        
        return response.text.strip() if response.text else "No transcription found."
        
    except Exception as e:
        # Cleanup on error
        try:
            os.unlink(tmp_path)
        except:
            pass
        return f"Error: {str(e)}"

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)