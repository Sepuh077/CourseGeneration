import os
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Elements:
    def __init__(self, video_course, folder_name: str, ext: str):
        self.video_course = video_course
        self.path = os.path.join(video_course.folder, folder_name)
        os.makedirs(self.path, exist_ok=True)

        self.ext = ext

    def send_message(self, message: str, index: int):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"project_{self.video_course.folder_name}",
            {
                "type": "send_generated_text",
                "message": message,
                "slide": index
            }
        )
    
    def send_skip_msg(self, index: int):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"project_{self.video_course.folder_name}",
            {
                "type": "send_skip_msg",
                "slide": index
            }
        )
    
    def send_error_msg(self, index: int):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"project_{self.video_course.folder_name}",
            {
                "type": "send_error_msg",
                "slide": index
            }
        )
    
    def relpath(self, index: int):
        return os.path.join(settings.MEDIA_URL, os.path.relpath(self[index], settings.MEDIA_ROOT)).replace('\\', '/')

    def __len__(self):
        return len(os.listdir(self.path))

    def __getitem__(self, index: int):
        return os.path.join(self.path, f"{index}.{self.ext}")
