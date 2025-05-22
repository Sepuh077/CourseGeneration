import os
from murf import Murf
import requests
from gtts import gTTS

from src import Elements
from src.constants import BASE_DIR


client = Murf(api_key=os.environ.get("MURF_API_KEY"))


class Audios(Elements):
    def __init__(self, video_course, texts: Elements, voice_name: str):
        super().__init__(video_course, "audios", "wav")

        self.texts = texts

        self.generate_audios()
    
    def generate_audios(self):
        for i in range(len(self.texts)):
            self.generate_audio(i)
    
    def generate_audio(self, index: int):
        if os.path.exists(self[index]):
            return
        
        text = self.texts.get(index)
        # audio_file = client.text_to_speech.generate(
        #     text = text,
        #     voice_id = "en-UK-theo",
        #     style = "Narration",
        #     multi_native_locale = "en-US"
        # ).audio_file

        # response = requests.get(audio_file)

        # if response.status_code == 200:
        #     with open(self[index], "wb") as f:
        #         f.write(response.content)

        try:
            audio = gTTS(text)
            audio.save(self[index])
        except AssertionError:
            pass
