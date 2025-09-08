import json
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor


def _analyze_single(transcript_path: str) -> Dict[str, object]:
    """A very naive analysis over the transcript JSON file."""
    with open(transcript_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    full_text = " ".join(seg.get("text", "") for seg in segments)
    word_count = len(full_text.split())
    # Naive scoring: one point for every 5 words, capped at 100
    score = min(100, word_count // 5)
    summary = full_text[:200]
    return {"score": score, "summary": summary}


def run_analysis(transcript_path: str) -> Dict[str, object]:
    """Public API for single transcript analysis."""
    return _analyze_single(transcript_path)


def batch_analysis(transcript_paths: List[str]) -> List[Dict[str, object]]:
    """Analyze multiple transcripts concurrently."""
    with ThreadPoolExecutor() as executor:
        return list(executor.map(_analyze_single, transcript_paths))
