import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4
from pydantic import BaseModel

from db.database import get_db
from db.models import Document

from rag.pipeline import pipeline

from rag.retriever import retrieve_ans

from rag.llm import llm
from rag.vectorstore import vector_store

from qdrant_client.models import Filter, FieldCondition, MatchValue

UPLOAD_DIR = Path("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024

class QueryRequest(BaseModel):
    request: str

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

    background_tasks.add_task(pipeline, document_id)

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
    
    # vector_store.client.delete(
    #      collection_name = vector_store.collection_name,
    #      points_selector=Filter(
    #           must=[FieldCondition(
    #                key="metadata,document_id",
    #                match=MatchValue(value=document_id)
    #           )]
    #      )
    # )
    
    return {
        "document_id": str(document_id),
        "message": "PDF deleted successfully"
    }
    

@app.get("/documents/{document_id}/status")
def get_status(document_id:str, db:Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.document_id == document_id).first()

    return {
         "status": doc.status
    }

@app.post("/query")
def query(queryRequest: QueryRequest):
     result = retrieve_ans(
          query=queryRequest.request , vector_store=vector_store, llm=llm, k=4
     )

     return {
          "query": queryRequest.request,
          "answer": result["answer"],
          "sources": result["sources"]
     }
