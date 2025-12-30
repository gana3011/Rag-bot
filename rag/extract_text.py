from pathlib import Path
import pdfplumber

UPLOAD_DIR = Path("uploads")

def extract(document_id):
    file_path = f"{UPLOAD_DIR}/{document_id}.pdf"
    document_pages = {}

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_num = page.page_number
            text = page.extract_text()
            document_pages[page_num] = text

    print(document_pages)
