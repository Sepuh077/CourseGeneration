import os
import json

from src import Elements
from src.helper import text_to_speech


class Audios(Elements):
    def __init__(self, video_course, texts: Elements, voice_id: str):
        super().__init__(video_course, "audios", "wav")

        self.data_path = os.path.join(self.video_course.folder, "data.json")

        self.texts = texts

        self.previous_data = self.get_previous_data()

        self.generate_audios(voice_id)
    
    def get_previous_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as file:
                data = json.loads(file.read())
            return data
        else:
            return []
    
    def update_previous_data(self):
        with open(self.data_path, "w") as file:
            file.write(json.dumps(self.previous_data))
    
    def generate_audios(self, voice_id):
        try:
            for i in range(len(self.texts)):
                self.generate_audio(i, voice_id)
            self.update_previous_data()
        except Exception as exc:
            self.update_previous_data()
            raise exc
    
    def compare_texts_by_index(self, index: int, text: str):
        return self.previous_data and len(self.previous_data) > index and self.previous_data[index]["text"] == text
    
    def compare_voice_ids_by_index(self, index: int, voice_id: str):
        return self.previous_data and len(self.previous_data) > index and self.previous_data[index]["voice_id"] == voice_id
    
    def generate_audio(self, index: int, voice_id: str):
        text = self.texts.get(index)
        
        if os.path.exists(self[index]) and self.compare_voice_ids_by_index(index, voice_id) and self.compare_texts_by_index(index, text):
            return

        text_to_speech(text, self[index], True, voice_id=voice_id)
        new_data = {
            "voice_id": voice_id,
            "text": text
        }
        if len(self.previous_data) > index:
            self.previous_data[index] = new_data
        else:
            self.previous_data.append(new_data)
