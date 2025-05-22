from django.http.response import JsonResponse
import json

from .models import VideoCourse as VC
from src import Texts, VideoCourse, Slides, Audios


def generate_texts(request, key: str):
    context = {}
    if request.method == "POST":
        vc = VC.objects.get(folder=key)
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        texts = Texts(video_course, slides)
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
        voice_name = request.POST.get("voice_name", "william")
        data = json.loads(request.POST['data'])

        vc = VC.objects.get(folder=key)

        video_course = VideoCourse(vc.folder, True)

        slides = Slides(video_course)
        texts = Texts(video_course, slides, data)
        audios = Audios(video_course, texts, voice_name)
        
        vc.audios_created = True
        vc.save()

        video_course.process(slides, audios)
    
    return JsonResponse(context)
