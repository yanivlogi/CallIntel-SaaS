from __future__ import annotations
import os
import json
from pathlib import Path
from typing import List, Tuple, Dict
from concurrent.futures import ThreadPoolExecutor

# Optional heavy imports. They may fail during tests if models are not installed
try:  # pragma: no cover - import errors are handled gracefully
    from faster_whisper import WhisperModel
except Exception:  # pragma: no cover
    WhisperModel = None  # type: ignore

try:  # pragma: no cover
    from pyannote.audio import Pipeline
except Exception:  # pragma: no cover
    Pipeline = None  # type: ignore

_whisper_model = None
_diarization_pipeline = None


def _load_models(engine: str) -> None:
    """Lazily load speech-to-text and diarization models."""
    global _whisper_model, _diarization_pipeline
    if engine == "whisper" and WhisperModel and _whisper_model is None:
        _whisper_model = WhisperModel("base")
    if Pipeline and _diarization_pipeline is None:
        token = os.getenv("HUGGINGFACE_TOKEN")
        _diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=token
        )


def _transcribe_single(
    audio_path: str,
    call_dir: str,
    engine: str = "whisper",
    enable_diarization: bool = True,
) -> Dict[str, str]:
    """Transcribe and optionally diarize a single audio file."""
    call_path = Path(call_dir)
    call_path.mkdir(parents=True, exist_ok=True)
    _load_models(engine)

    transcript = []
    if _whisper_model:
        segments, _ = _whisper_model.transcribe(audio_path)
        for seg in segments:
            transcript.append(
                {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
            )
    else:  # pragma: no cover - fallback when model isn't available
        transcript.append({"start": 0, "end": 0, "text": "[unavailable]"})

    result: Dict[str, List[Dict[str, float | str]]] = {"segments": transcript}

    if enable_diarization and _diarization_pipeline:
        diarization = _diarization_pipeline(audio_path)
        speakers = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speakers.append(
                {"speaker": speaker, "start": turn.start, "end": turn.end}
            )
        result["speakers"] = speakers

    transcript_path = call_path / "transcript.json"
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return {"transcript_path": str(transcript_path), "call_dir": str(call_path)}


def run_transcription_and_diarization(
    audio_path: str,
    call_dir: str,
    engine: str = "whisper",
    enable_diarization: bool = True,
) -> Dict[str, str]:
    """Public wrapper used by the API for a single file."""
    return _transcribe_single(audio_path, call_dir, engine, enable_diarization)


def batch_transcription(
    items: List[Tuple[str, str]],
    engine: str = "whisper",
    enable_diarization: bool = True,
) -> List[Dict[str, str]]:
    """Process multiple audio files concurrently.

    Each item is a tuple of (audio_path, call_dir).
    """
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                _transcribe_single, audio, directory, engine, enable_diarization
            )
            for audio, directory in items
        ]
        return [f.result() for f in futures]
