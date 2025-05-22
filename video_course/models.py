import os

from django.db import models
from django.conf import settings

from src.constants import PROJECT_FOLDER, RESULT_MP4


# Create your models here.
class VideoCourse(models.Model):
    title = models.CharField(max_length=64)
    folder = models.CharField(max_length=128)

    images_created = models.BooleanField(default=False)
    texts_created = models.BooleanField(default=False)
    audios_created = models.BooleanField(default=False)

    def get_video_path(self):
        path = os.path.join(settings.MEDIA_ROOT, PROJECT_FOLDER, self.folder, RESULT_MP4)
        return os.path.join(settings.MEDIA_URL, PROJECT_FOLDER, self.folder, RESULT_MP4) if os.path.exists(path) else None


class Voices(models.Model):
    voice_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    avatar = models.TextField()
