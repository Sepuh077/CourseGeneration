import os
from django.conf import settings


class Elements:
    def __init__(self, project_path: str, folder_name: str, ext: str):
        self.path = os.path.join(project_path, folder_name)
        os.makedirs(self.path, exist_ok=True)

        self.ext = ext
    
    def relpath(self, index: int):
        return os.path.join(settings.MEDIA_URL, os.path.relpath(self[index], settings.MEDIA_ROOT)).replace('\\', '/')

    def __len__(self):
        return len(os.listdir(self.path))

    def __getitem__(self, index: int):
        return os.path.join(self.path, f"{index}.{self.ext}")
