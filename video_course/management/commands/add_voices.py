from django.core.management.base import BaseCommand
from django.conf import settings

import json
import requests
import os

from video_course.models import Voice


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        response = requests.get("https://api.murf.ai/v1/speech/voices", headers={
            "api-key": os.environ.get("MURF_API_KEY"),
        })

        avatar_url = "https://murf.ai/public-assets/home/avatars/{}.jpg"

        data = list(filter(lambda x: x['locale'].lower() == "en-us" and x["accent"] == "US & Canada", response.json()))

        for voice in data:
            voice_id = voice["voiceId"]
            name = voice["displayName"].split()[0]
            avatar = avatar_url.format(name)
            Voice.objects.create(
                voice_id=voice_id,
                name=name,
                avatar=avatar
            )
            
