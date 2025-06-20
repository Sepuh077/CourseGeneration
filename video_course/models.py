import os

from django.db import models
from django.conf import settings
from datetime import datetime

from src.constants import PROJECT_FOLDER, RESULT_MP4


class VideoCourse(models.Model):
    title = models.CharField(max_length=64)
    folder = models.CharField(max_length=128)

    created = models.DateTimeField(default=datetime.now)

    video_created_time = models.DateTimeField(blank=True, null=True)

    def get_video_path(self):
        path = os.path.join(settings.MEDIA_ROOT, PROJECT_FOLDER, self.folder, RESULT_MP4)
        return os.path.join(settings.MEDIA_URL, PROJECT_FOLDER, self.folder, RESULT_MP4) if os.path.exists(path) else None
    
    def create_video(self):
        self.video_created_time = datetime.now()
        self.save()

    class Meta:
        ordering = ['-created']


class Voice(models.Model):
    voice_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    avatar = models.TextField()