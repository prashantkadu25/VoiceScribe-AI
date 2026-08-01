from streamlit_webrtc import webrtc_streamer, WebRtcMode
import queue
import numpy as np

audio_buffer = []
audio_queue = queue.Queue()

class AudioProcessor:

    def recv(self, frame):

        audio = frame.to_ndarray()

        # (1,1920) -> (1920,)
        audio = audio.flatten()

        audio_buffer.append(audio)

        return frame


def start_live_audio():

    webrtc_streamer(
        key="live-audio",
        mode=WebRtcMode.SENDONLY,
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        audio_processor_factory=AudioProcessor,
    )

    return audio_queue

def get_audio_chunk():

    global audio_buffer

    if len(audio_buffer) < 50:
        return None

    chunk = np.concatenate(audio_buffer)

    audio_buffer = []

    return chunk.tobytes()