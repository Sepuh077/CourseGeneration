import torchaudio
import os
from tortoise.utils.audio import load_voice
from tortoise.api import TextToSpeech
from murf import Murf
import requests
from gtts import gTTS

from src import Elements
from src.constants import BASE_DIR


client = Murf(api_key=os.environ.get("MURF_API_KEY"))


class Audios(Elements):
    def __init__(self, project_path: str, texts: Elements, voice_name: str):
        super().__init__(project_path, "audios", "wav")

        self.texts = texts

        # os.chdir(os.path.join(BASE_DIR, "tortoise-tts"))
        
        # self.tts = TextToSpeech()
        # self.voice_samples, self.conditioning_latents = load_voice(voice_name)

        self.generate_audios()
    
    def generate_audios(self):
        for i in range(len(self.texts)):
            self.generate_audio(i)
    
    def generate_audio(self, index: int):
        if os.path.exists(self[index]):
            return
        
        text = self.texts.get(index)
        # gen = self.tts.tts_with_preset(text, voice_samples=self.voice_samples, conditioning_latents=self.conditioning_latents, preset="ultra_fast")
        # torchaudio.save(self[index], gen.squeeze(0).cpu(), 24000)

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
