from django.core.management.base import BaseCommand
from django.conf import settings

import json
import os

from video_course.models import Voice
from src.helper import text_to_speech


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        avatar_url = "https://murf.ai/public-assets/home/avatars/{}.jpg"

        with open(os.path.join(settings.BASE_DIR, "video_course/data/voices.json"), "r") as f:
            data = json.loads(f.read())
        for voice in data:
            voice_id = voice["voiceId"]
            name = voice["displayName"].split()[0]
            avatar = avatar_url.format(name)
            Voice.objects.update_or_create(
                voice_id=voice_id,
                defaults=dict(
                    name=name,
                    avatar=avatar
                )
            )
            
            audio_path = os.path.join(settings.BASE_DIR, "static", "voices", f"{name}.wav")
            if not os.path.exists(audio_path):
                text_to_speech(f"Hello, my name is {name}.", audio_path, raise_exc=True, voice_id=voice_id)
