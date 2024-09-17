from fpdf import FPDF
from PIL import Image

"""
SET OF FUNCTIONS TO:

- Translate locations of elements
- Generate the required SVGs using FPDF such as text
- Append them to the pdf file
- Return the pdf file
"""


def create_pdf_object():
    pdf = FPDF()
    return pdf


def translate_locations_pdf(element_map):
    pass


def svg_generator(temp_label_paths: list[str]):
    pass


def pdf_generator(pdf, pdf_path: str, temp_label_paths: list[str]) -> None:
    for label_path in temp_label_paths:
        append_pdf(pdf, label_path)
    pdf.output(pdf_path)
    return pdf


def append_pdf(pdf: object, label_path: str) -> None:
    if not label_path.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp")):
        return
    img = Image.open(label_path)
    img_width, img_height = img.size
    pdf.add_page(orientation="portrait", format=(img_width, img_height))
    pdf.image(label_path, x=0, y=0, w=img_width, h=img_height)
