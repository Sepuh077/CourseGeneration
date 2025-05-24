import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GeneratedTextConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"project_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def send_error_msg(self, event):
        slide = event["slide"]
        self.send(
            text_data=json.dumps({
                "error": True,
                "slide": slide
            })
        )
    
    def send_skip_msg(self, event):
        slide = event["slide"]
        self.send(
            text_data=json.dumps({
                "skip": True,
                "slide": slide
            })
        )

    def send_generated_text(self, event):
        message = event["message"]
        slide = event["slide"]

        self.send(
            text_data=json.dumps({
                "message": message,
                "slide": slide
            })
        )
