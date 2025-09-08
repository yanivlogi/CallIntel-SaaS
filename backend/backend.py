from fastapi import FastAPI, UploadFile, File
from typing import List, Tuple
import uuid, shutil
from pathlib import Path
from analysis.transcribe_and_diarize import (
    run_transcription_and_diarization,
    batch_transcription,
)

app = FastAPI(title="CallIntel API")

CALLS_DIR = Path("storage/calls")
CALLS_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a single audio file."""
    call_id = str(uuid.uuid4())
    call_dir = CALLS_DIR / call_id
    call_dir.mkdir(parents=True, exist_ok=True)

    audio_path = call_dir / file.filename
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = run_transcription_and_diarization(
        audio_path=str(audio_path),
        call_dir=str(call_dir),
        engine="whisper",
        enable_diarization=True,
    )

    return {"call_id": call_id, "result": result}


@app.post("/upload_batch")
async def upload_batch(files: List[UploadFile] = File(...)):
    """Upload and process multiple audio files concurrently."""
    items: List[Tuple[str, str]] = []
    call_ids: List[str] = []

    for file in files:
        call_id = str(uuid.uuid4())
        call_dir = CALLS_DIR / call_id
        call_dir.mkdir(parents=True, exist_ok=True)
        audio_path = call_dir / file.filename
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        call_ids.append(call_id)
        items.append((str(audio_path), str(call_dir)))

    results = batch_transcription(
        items, engine="whisper", enable_diarization=True
    )
    return {"call_ids": call_ids, "results": results}
