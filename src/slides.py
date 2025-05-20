import fitz
import os
import base64

from src import Elements


class Slides(Elements):
    def __init__(self, project_path: str, document: str):
        super().__init__(project_path, "images", "jpg")

        self.seperate_images(document)
    
    def seperate_images(self, document: str):
        if document.endswith(".pdf"):
            self.pdf_to_images(document)
        else:
            raise ValueError("The document file type should be PDF")

    def pdf_to_images(self, document):
        pdf_document = fitz.open(document)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            output_file = self[page_num]
            pix.save(output_file)
            print(f"Saved {output_file}")
        
        pdf_document.close()
        print("All pages saved as images!")

    def image_to_base64(self, index):
        with open(self[index], "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def get_base64(self, index):
        return self.image_to_base64(index)
