from rag.extract_text import extract
from rag.splitter import split_text
from rag.embedder import embed_text
from db.database import SessionLocal
from db.models import Document

def pipeline(document_id):
    print("in pipeline")
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(document_id == document_id).first()
        if not doc:
            return
        
        doc.status = "PROCESSING"
        db.commit()

        documents = extract(document_id)
        splits = split_text(documents)
        embed_text(splits)

        doc.status = "COMPLETED"
        db.commit()
        print("over")

    except Exception:
        doc.status = "FAILED"
        db.commit()
        raise

    finally:
        db.close()
    