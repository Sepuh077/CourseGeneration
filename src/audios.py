import torchaudio
import os
from tortoise.utils.audio import load_voice
from tortoise.api import TextToSpeech

from src import Elements
from src.constants import BASE_DIR


class Audios(Elements):
    def __init__(self, project_path: str, texts: Elements, voice_name: str):
        super().__init__(project_path, "audios", "wav")

        self.texts = texts

        os.chdir(os.path.join(BASE_DIR, "tortoise-tts"))
        
        self.tts = TextToSpeech()
        self.voice_samples, self.conditioning_latents = load_voice(voice_name)

        self.generate_audios()
    
    def generate_audios(self):
        for i in range(len(self.texts)):
            self.generate_audio(i)
    
    def generate_audio(self, index: int):
        if os.path.exists(self[index]):
            return
        with open(self.texts[index], "r") as file:
            text = file.read()
        gen = self.tts.tts_with_preset(text, voice_samples=self.voice_samples, conditioning_latents=self.conditioning_latents, preset="ultra_fast")
        torchaudio.save(self[index], gen.squeeze(0).cpu(), 24000)
