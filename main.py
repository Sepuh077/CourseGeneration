from argparse import ArgumentParser
from dotenv import load_dotenv

load_dotenv(override=True)

from src import VideoCourse, Slides, Texts, Audios, Videos


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-d', '--document', help="The slides path (currently only supports .pdf filetype)", required=True)
    parser.add_argument('--data', help="The texts for each slide in json format, if not provided, the text will be generated using LLM", required=False)
    parser.add_argument('-n', '--name', help="The name of the course, if not provided will be generated automatically", default="Project")
    parser.add_argument('-v', '--voice', help="The name of the voice from tortoise TTS, defaul 'William'", default="william")
    parser.add_argument('-w', '--wav2lip', action="store_true", help="Use wav2lip to add professor image, by default False", default=False)
    parser.add_argument('-p', '--professor', help="The image or video of professor, only needed if wav2lip=True", required=False)
    parser.add_argument('-e', '--exists-ok', action="store_true", help="If False, it will create non existing folder by indexing the name", default=False)

    args = parser.parse_args()

    video_course = VideoCourse(args.name, args.exists_ok)

    slides = Slides(video_course.folder, args.document)
    texts = Texts(video_course.folder, slides, args.data, args.data == None)
    audios = Audios(video_course.folder, texts, args.voice)

    if args.wav2lip:
        videos = Videos(video_course.folder, audios, args.professor)
    else:
        videos = None

    video_course.process(slides, videos or audios)
