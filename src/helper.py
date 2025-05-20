import fitz
import os
import base64


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
