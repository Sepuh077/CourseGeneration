from django.http.response import JsonResponse
from django.urls import reverse

import json

from time import sleep

from .models import VideoCourse as VC, Voice
from src import Texts, VideoCourse, Slides, Audios


def get_voices(request):
    voices = []
    if request.method == "GET":
        for voice in Voice.objects.all():
            voices.append({
                "id": voice.voice_id,
                "name": voice.name,
                "avatar": voice.avatar
            })
    return JsonResponse({"voices": voices})



def regenerate_text(request, key: str, index: int):
    context = {}
    if request.method == "POST":
        force = request.POST.get("force") in [True, 'true', 'True']
        data = json.loads(request.POST.get("data", []))
        vc = VC.objects.get(folder=key)
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        texts = Texts(video_course, slides, data)
        context["text"], context["skipped"] = texts.regenerate_text(index, force)
        vc.texts_created = True
        vc.save()
    
    return JsonResponse(context)


def update_texts(request, key: str):
    context = {}
    if request.method == "POST":
        data = json.loads(request.POST['data'])
        vc = VC.objects.get(folder=key)
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        Texts(video_course, slides, data)
    
    return JsonResponse(context)


def generate_video(request, key: str):
    context = {}
    if request.method == "POST":
        voice_id = request.POST.get("voice_id") or "william"

        data = json.loads(request.POST['data'])

        vc = VC.objects.get(folder=key)

        video_course = VideoCourse(vc.folder, True)

        slides = Slides(video_course)
        texts = Texts(video_course, slides, data)
        audios = Audios(video_course, texts, voice_id)
        video_course.process(slides, audios)

        vc.create_video()

        context["link"] = reverse("show-video", kwargs={"key": key})
    
    return JsonResponse(context)
