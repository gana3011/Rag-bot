from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await file.close()

    return {
        "filename": file.filename,
        "stored_at": str(file_path)
    }