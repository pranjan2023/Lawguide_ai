from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.summarizer import generate_summary
from app.database import SessionLocal
from app.models import Document
import fitz
import os
import shutil
import textwrap

app = FastAPI()
MAX_CHUNK_SIZE = 1000

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-and-summarize/")
async def upload_and_summarize(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"temp_files/{file.filename}"
    os.makedirs("temp_files", exist_ok=True)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with fitz.open(file_location) as doc:
            num_pages = doc.page_count
            text = ""
            for page in doc:
                text += page.get_text()
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

    try:
        chunks = textwrap.wrap(text, MAX_CHUNK_SIZE)
        print(chunks)
        summaries = [generate_summary(chunk).strip() for chunk in chunks if chunk.strip()]
        final_summary = " ".join(summaries)
    except Exception as e:
        return {"error": f"Failed to summarize text: {str(e)}"}

    os.remove(file_location)

    doc_record = Document(
        filename=file.filename,
        num_pages=num_pages,
        content=text,
        summary=final_summary
    )
    db.add(doc_record)
    db.commit()
    db.refresh(doc_record)

    return {
        "id": doc_record.id,
        "filename": doc_record.filename,
        "num_pages": num_pages,
        "summary": final_summary
    }