import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4

from db.database import get_db
from db.models import Document

from rag.extract_text import extract


UPLOAD_DIR = Path("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024

app = FastAPI()


@app.post("/upload-pdf")
async def create_upload_file(file: UploadFile, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only pdf files are allowed")
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    document_id = uuid4()
        
    file_path = f"{UPLOAD_DIR}/{document_id}.pdf"

    try:

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

    except Exception:
                raise HTTPException(status_code=500, detail="Failed to save file")
    

    document = Document(
            document_id=document_id,
            name=file.filename,
            storage_path=file_path,
            status="UPLOADED"
        )

    try:
        db.add(document)
        db.commit()
    except Exception:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail="Database error")
    
    uploaded_document = db.query(Document).filter(Document.document_id == document_id).first()
    if uploaded_document:
         uploaded_document.status = "PROCESSING"

    background_tasks.add_task(extract, document_id)

    return {
        "document_id": str(document_id),
        "message": "PDF uploaded successfully"
    }

@app.delete("/delete-pdf/{document_id}")
async def delete_pdf(document_id:str, db: Session = Depends(get_db)):
    
    file_path = f"{UPLOAD_DIR}/{document_id}.pdf"

    try:
        delete_document = db.query(Document).filter(Document.document_id == document_id)
        delete_document.delete()
        db.commit()
        os.remove(file_path)

    except Exception:
         raise HTTPException(status_code=500, detail="Database error")

    return {
        "document_id": str(document_id),
        "message": "PDF deleted successfully"
    }
    
