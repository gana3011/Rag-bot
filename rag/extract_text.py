from pathlib import Path
import pdfplumber
from langchain_core.documents import Document
from splitter import split_text

UPLOAD_DIR = Path("uploads")

def extract(document_id):
    file_path = f"{UPLOAD_DIR}/{document_id}.pdf"
    documents = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            doc = Document(
                page_content= page.extract_text() or "",
                metadata = {
                    "document_id": document_id,
                    "page_number": page.page_number
                }
            )
            documents.append(doc)
        

    split_text(documents)

extract("2778e84b-6e39-43cc-b628-9abd5141edcb")