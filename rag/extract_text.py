from pathlib import Path
import pdfplumber
from langchain_core.documents import Document

UPLOAD_DIR = Path("uploads")

def extract(document_id):
    file_path = f"{UPLOAD_DIR}/{document_id}.pdf"
    documents = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            doc = Document(
                page_content= page.extract_text() or "",
                metadata = {
                    "document_id": str(document_id),
                    "page_number": page.page_number
                }
            )
            documents.append(doc)
        

    return documents
