from django.shortcuts import render, redirect
from django.http.response import Http404
from django.core.exceptions import ObjectDoesNotExist

from src import VideoCourse, Slides, Texts
from .models import VideoCourse as VC

# Create your views here.
def upload_slides(request):
    if request.method == "POST":
        VC.objects.all().delete()
        document = request.FILES['document']
        name = request.POST.get("name") or ".".join(document.name.split('.')[:-1]) or "Project"

        video_course = VideoCourse(name)

        vc = VC.objects.create(
            title=name,
            folder=video_course.folder_name
        )
        Slides(video_course, document.read())
        vc.save()

        return redirect('process', key=vc.folder)
    
    return render(request, "video_course/upload.html")


def process_video_course(request, key):
    context = {
        'data': []
    }

    try:
        vc = VC.objects.get(folder=key)
    except ObjectDoesNotExist as exc:
        raise Http404("Page not found!")
    if request.method == "GET":
        video_course = VideoCourse(vc.folder, True)
        slides = Slides(video_course)
        texts = Texts(video_course, slides)

        for i in range(len(slides)):
            context['data'].append({
                'image': slides.relpath(i),
                'text': texts.get(i)
            })

        context['video_path'] = vc.get_video_path()
        context['title'] = vc.title

    return render(request, "video_course/process.html", context=context)


def show_video(request, key):
    context = {}

    vc = VC.objects.get(folder=key)
    if request.method == "GET":
        context['video_path'] = vc.get_video_path()
        if not context['video_path']:
            raise Http404("Page not found!")
        context['key'] = key

    return render(request, "video_course/video.html", context=context)
