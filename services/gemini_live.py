import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


class GeminiLive:

    def __init__(self):

        self.session = None

        self.response_text = ""

    async def connect(self):

        self.session = await client.aio.live.connect(
            model="gemini-live-2.5-flash-preview",
            config=types.LiveConnectConfig(
                response_modalities=["TEXT"]
            )
        )

        print("✅ Connected to Gemini Live")

    async def send_audio(self, pcm_audio):

        await self.session.send_realtime_input(
            audio=types.Blob(
                data=pcm_audio,
                mime_type="audio/pcm;rate=16000"
            )
        )

    async def receive(self):

        async for response in self.session.receive():

            if response.text:

                print(response.text)

                self.response_text += response.text

        return self.response_text

    async def close(self):

        if self.session:

            await self.session.close()