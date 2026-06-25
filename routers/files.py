from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_file(filename: str):
    # this runs AFTER response is sent
    print(f"Processing {filename}...")
    # in real world: extract text, run AI, send email
    print(f"Done processing {filename}")

@router.post("/upload")
def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # save file to disk
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # add processing to background — runs after response
    background_tasks.add_task(process_file, file.filename)

    return {
        "filename": file.filename,
        "message": "File uploaded. Processing started."
    }