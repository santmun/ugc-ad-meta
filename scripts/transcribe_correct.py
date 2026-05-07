#!/usr/bin/env python3
"""Transcribe los 6 videos del anuncio con Whisper español y los deja listos
para el build_composition.

Uso:
  python3 transcribe_correct.py --project <hyperframes-project-dir>

Requiere que existan scene-{1..6}.mp4 en el project-dir.
Genera transcript-scene-{1..6}.json (raw — sin correcciones).
Las correcciones se aplican después en build_composition.py vía glossary.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--language", default="es")
    ap.add_argument("--model", default="small")
    args = ap.parse_args()

    proj = Path(args.project)
    if not proj.exists():
        print(f"ERROR: project dir not found: {proj}")
        sys.exit(1)

    for i in range(1, 7):
        scene = proj / f"scene-{i}.mp4"
        if not scene.exists():
            print(f"WARN: missing {scene}, skipping")
            continue

        print(f"=== Transcribing scene-{i} ===")
        cmd = [
            "npx", "hyperframes", "transcribe", str(scene),
            "--model", args.model, "--language", args.language,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=proj)
        if r.returncode != 0:
            print(f"  ERROR: {r.stderr[:300]}")
            continue

        # hyperframes transcribe writes transcript.json — rename
        src = proj / "transcript.json"
        dst = proj / f"transcript-scene-{i}.json"
        if src.exists():
            shutil.move(str(src), str(dst))
            words = json.loads(dst.read_text())
            print(f"  ✓ {len(words)} words")
        else:
            print(f"  WARN: no transcript.json produced")

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
