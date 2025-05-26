import os
import subprocess
from django.conf import settings

from src import Elements


class Videos(Elements):
    def __init__(self, video_course, audios: Elements, prof_path: str):
        super().__init__(video_course, "videos", "mp4")

        self.audios = audios
        self.checkpoint_path = os.path.join(settings.BASE_DIR, "Wav2Lip/checkpoints/wav2lip_gan.pth")

        self.check_image_path(prof_path)
        self.generate_videos()
    
    def check_image_path(self, prof_path):
        if prof_path is None or not os.path.exists(prof_path):
            raise FileNotFoundError("The path does not exists!")
        self.image = prof_path
    
    def generate_videos(self):
        for index in range(len(self.audios)):
            self.generate_video(index)

    def generate_video(self, index: int):
        if os.path.exists(self[index]) or not os.path.exists(self.audios[index]):
            return
        command = f"python {os.path.join(settings.BASE_DIR, 'Wav2Lip/inference.py')} --checkpoint_path {self.checkpoint_path} --face {self.image} --audio {self.audios[index]} --outfile {self[index]} --face_det_batch_size 4"
        subprocess.run(command, shell=True)
