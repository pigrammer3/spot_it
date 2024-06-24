from pathlib import Path

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.utils import ImageReader
from PIL import Image
from tqdm import tqdm

CARD_WIDTH = 3.5 * inch
CARDS_ON_PAGE_HORIZ = 2
CARDS_ON_PAGE_VERT = 3
HORIZ_SPACING = (LETTER[0] - CARDS_ON_PAGE_HORIZ * CARD_WIDTH) / (
    CARDS_ON_PAGE_HORIZ + 1
)
VERT_SPACING = (LETTER[1] - CARDS_ON_PAGE_VERT * CARD_WIDTH) / (CARDS_ON_PAGE_VERT + 1)


def put_on_pdf(cards: list[Image.Image], output_path: Path):
    pdf = Canvas(str(output_path.absolute()), pagesize=LETTER)
    imgs_on_cur_page = 0
    for image in tqdm(cards, desc="PDFing cards"):
        if imgs_on_cur_page == CARDS_ON_PAGE_HORIZ * CARDS_ON_PAGE_VERT:
            pdf.showPage()
            imgs_on_cur_page = 0
        x = HORIZ_SPACING + (CARD_WIDTH + HORIZ_SPACING) * (
            imgs_on_cur_page % CARDS_ON_PAGE_HORIZ
        )
        y = LETTER[1] - (CARD_WIDTH + VERT_SPACING) * (
            1 + imgs_on_cur_page // CARDS_ON_PAGE_HORIZ
        )
        pdf.drawImage(ImageReader(image), x, y, width=CARD_WIDTH, height=CARD_WIDTH)
        imgs_on_cur_page += 1
    pdf.save()
