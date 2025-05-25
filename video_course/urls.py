from django.urls import path

from .views import upload_slides, process_video_course, show_video
from .apis import generate_texts, update_texts, generate_video, regenerate_text, get_voices


urlpatterns = [
    path('upload', upload_slides, name='upload'),
    path('process/<str:key>/', process_video_course, name='process'),
    path('process/<str:key>/generate-texts/', generate_texts),
    path('process/<str:key>/update-texts/', update_texts),
    path('process/<str:key>/generate-video/', generate_video),
    path('process/<str:key>/regenerate-text-<int:index>/', regenerate_text),
    path('get-voices/', get_voices),
    path('process/<str:key>/finished/', show_video, name="show-video")
]
