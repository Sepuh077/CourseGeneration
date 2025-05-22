import os
import re
from pathlib import Path
from django.conf import settings
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip

from src.constants import PROJECT_FOLDER, RESULT_MP4
from src import Elements


class VideoCourse:
    def __init__(self, name: str, exists_ok: bool = False):
        self.name = name
        self.folder = self.set_project_path(name, exists_ok)
        self.folder_name = Path(self.folder).name
    
    def set_project_path(self, name: str, exists_ok: bool):
        folder = os.path.join(settings.MEDIA_ROOT, PROJECT_FOLDER)
        name = re.sub(r'[^\w]', '', name, flags=re.UNICODE)
        project_path = os.path.join(folder, name)

        if not exists_ok:
            i = 0
            while os.path.exists(project_path):
                i += 1
                project_path = os.path.join(folder, name + f"-{i}")
        return project_path
    
    def process(self, slides: Elements, medias: Elements):
        videoclips = []
        for index in range(len(slides)):
            videoclips.append(
                self.combine_slide_and_media(
                    slides[index],
                    medias[index]
                )
            )

        result_path = os.path.join(self.folder, RESULT_MP4)

        videoclips = list(filter(lambda x: x, videoclips))
        concatenate_videoclips(videoclips).write_videofile(result_path)

        return result_path
    
    def combine_slide_and_media(self, image_path: str, media_path: str):
        if not os.path.exists(media_path):
            return
        if media_path.endswith("wav"):
            return self.combine_slide_and_audio(image_path, media_path)
        elif media_path.endswith("mp4"):
            return self.combine_slide_and_video(image_path, media_path)
        else:
            raise ValueError("The media format is not recognized!")
        
    def combine_slide_and_audio(self, image_path, audio_path):
        image = ImageClip(image_path)
        audio = AudioFileClip(audio_path)

        image = image.with_duration(audio.duration + 0.5).with_audio(audio).with_fps(24)

        return image

    def combine_slide_and_video(self, image_path, video_path):
        image = ImageClip(image_path)
        video = VideoFileClip(video_path)

        video_resized = video.resized(height=200)

        video_positioned = video_resized.with_position(("right", "top"))

        image_duration = video.duration
        image = image.with_duration(image_duration)

        combined = CompositeVideoClip([image, video_positioned])

        return combined
