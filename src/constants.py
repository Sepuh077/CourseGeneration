import os
from murf import Murf

PROJECT_FOLDER = "projects"
RESULT_MP4 = "result.mp4"

MURF_CLIENT = Murf(api_key=os.environ.get("MURF_API_KEY"))
