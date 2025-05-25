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


def generate_texts(request, key: str):
    context = {}
    if request.method == "POST":
        data = json.loads(request.POST.get("data", []))
        vc = VC.objects.get(folder=key)
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        texts = Texts(video_course, slides, data)
        texts.generate_texts_for_slides()
        vc.texts_created = True
        vc.save()
    
    return JsonResponse(context)


def regenerate_text(request, key: str, index: int):
    context = {}
    if request.method == "POST":
        vc = VC.objects.get(folder=key)
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        texts = Texts(video_course, slides)
        context["text"] = texts.regenerate_text(index)
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
        vc.texts_created = True
        vc.save()
    
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
        
        vc.audios_created = True
        vc.save()

        video_course.process(slides, audios)

        context["link"] = reverse("show-video", kwargs={"key": key})
    
    return JsonResponse(context)
