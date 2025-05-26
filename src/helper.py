import fitz
import os
import base64
import requests
from gtts import gTTS
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from src.constants import MURF_CLIENT


def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def pdf_to_images(pdf_path, output_folder):
    """
    Converts each page of a PDF to an image and saves them in the specified output folder.
    
    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to the folder where images will be saved.
    """
    pdf_document = fitz.open(pdf_path)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate through pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load the page
        pix = page.get_pixmap()  # Render the page as an image
        output_file = os.path.join(output_folder, f"{page_num + 1}.jpg")
        pix.save(output_file)  # Save the image
        print(f"Saved {output_file}")
    
    pdf_document.close()
    print("All pages saved as images!")


def text_to_speech(text: str, audio_path: str, test: bool = False, raise_exc: bool = False, voice_id: str = ""):
    try:
        if not test:
            audio_file = MURF_CLIENT.text_to_speech.generate(
                text = text,
                voice_id = voice_id,
            ).audio_file

            response = requests.get(audio_file)

            if response.status_code == 200:
                with open(audio_path, "wb") as f:
                    f.write(response.content)
        else:
            audio = gTTS(text)
            audio.save(audio_path)
    except Exception as exc:
        if raise_exc:
            raise exc


def image_to_base64(img_path, format='jpeg'):
    with open(os.path.join(settings.BASE_DIR, img_path), 'rb') as image:
        encoded_string = base64.b64encode(image.read()).decode()
        return f'data:image/{format};base64,' + encoded_string


def send_email(request, subject, mail_text, to, context={}, is_template=True):
    from_email = settings.EMAIL_HOST_USER

    # context['logo_url'] = request.build_absolute_uri('/static/images/logo/logo.png')# image_to_base64('static/images/logo/logo-name-bottom.webp')
    # context['contact_url'] = request.build_absolute_uri('/#contact')
    context['contact_email'] = from_email

    if is_template:
        mail_text = render_to_string(mail_text, context)

    send_mail(subject, mail_text, from_email, to, fail_silently=False, html_message=mail_text)

