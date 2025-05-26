import os

from src import Elements
from src.helper import text_to_speech


class Audios(Elements):
    def __init__(self, video_course, texts: Elements, voice_id: str):
        super().__init__(video_course, "audios", "wav")

        self.texts = texts

        self.generate_audios(voice_id)
    
    def generate_audios(self, voice_id):
        for i in range(len(self.texts)):
            self.generate_audio(i, voice_id)
    
    def generate_audio(self, index: int, voice_id: str):
        if os.path.exists(self[index]):
            return
        
        text = self.texts.get(index)

        text_to_speech(text, self[index], True, voice_id=voice_id)
