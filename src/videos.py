import os
import subprocess

from src import Elements
from src.constants import BASE_DIR


class Videos(Elements):
    def __init__(self, project_path: str, audios: Elements, prof_path: str):
        super().__init__(project_path, "videos", "mp4")

        self.audios = audios
        self.checkpoint_path = os.path.join(BASE_DIR, "Wav2Lip/checkpoints/wav2lip_gan.pth")

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
        if os.path.exists(self[index]):
            return
        command = f"python {os.path.join(BASE_DIR, 'Wav2Lip/inference.py')} --checkpoint_path {self.checkpoint_path} --face {self.image} --audio {self.audios[index]} --outfile {self[index]} --face_det_batch_size 4"
        subprocess.run(command, shell=True)
