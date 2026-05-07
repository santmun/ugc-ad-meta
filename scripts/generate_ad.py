#!/usr/bin/env python3
"""Orquestador end-to-end: genera 6 videos UGC con Kling 3.0 a partir de un guion JSON.

Uso:
  python3 generate_ad.py --config <user-config.json> --script <script.json> --out <dir>

script.json format:
{
  "scenes": [
    {"n": 1, "dialogue": "...", "vibe": "..."},
    {"n": 2, ...}, ...
  ]
}

Genera 6 videos en <dir>/scene-{1..6}.mp4 secuencialmente con backoff.
"""
import argparse
import json
import subprocess
import time
import urllib.request
from pathlib import Path


def build_prompt(dialogue: str, vibe: str, idioma_desc: str, extra: str = "") -> str:
    return (
        f'The person speaks this Spanish dialogue with perfect lip-sync, reading '
        f'the text EXACTLY as written: "{dialogue}" '
        f'CRITICAL RULES: '
        f'(1) Spoken language must be {idioma_desc}. NOT European Spanish from Spain. '
        f'(2) Read PHONETICALLY. Do NOT translate words to English. '
        f'"punto com" stays "punto com". "i a" = two letters separately, NOT "ya". '
        f'"Klaud" = English "cloud". "app" = English "app". Do NOT add extra syllables. '
        f'(3) Vibe: {vibe}. {extra} '
        f'(4) Articulate two-word combos with same consonant SEPARATELY. '
        f'(5) Subtle natural head movements. NO theatrical gestures. '
        f'NO bringing hands to face. Realistic everyday selfie behavior. '
        f'(6) End each sentence with rising/sustained tone (NOT flat-falling). '
        f'(7) Background, hair, outfit IDENTICAL to start frame. '
        f'Selfie UGC vertical 9:16.'
    )


SUPPORTED_VIDEO_MODELS = ("kling3_0", "seedance_2_0")


def generate_scene(scene: dict, model_uuid: str, idioma_desc: str, out_path: Path,
                   video_model: str = "kling3_0", duration: int = 5,
                   max_retries: int = 3) -> tuple[str, str]:
    if video_model not in SUPPORTED_VIDEO_MODELS:
        raise ValueError(
            f"video_model must be one of {SUPPORTED_VIDEO_MODELS}, got {video_model}"
        )
    n = scene["n"]
    prompt = build_prompt(
        scene["dialogue"],
        scene["vibe"],
        idioma_desc,
        scene.get("extra", "")
    )
    cmd = [
        "higgsfield", "generate", "create", video_model,
        "--prompt", prompt,
        "--aspect_ratio", "9:16",
        "--duration", str(duration),
        "--image", model_uuid,
        "--wait", "--json",
    ]
    # Seedance has resolution param; Kling does not.
    if video_model == "seedance_2_0":
        cmd += ["--resolution", "720p"]
    for attempt in range(1, max_retries + 1):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            if r.returncode == 0:
                data = json.loads(r.stdout)
                url = data[0]["result_url"]
                urllib.request.urlretrieve(url, out_path)
                return ("OK", str(out_path))
            err = (r.stderr[:200] or r.stdout[:200])
            print(f"  scene {n} attempt {attempt} failed: {err}", flush=True)
            if attempt < max_retries:
                time.sleep(attempt * 30)
        except Exception as e:
            print(f"  scene {n} attempt {attempt} exception: {e}", flush=True)
            if attempt < max_retries:
                time.sleep(attempt * 30)
    return ("ERROR", f"failed after {max_retries} attempts")


IDIOMA_MAP = {
    "es-LATAM": "LATIN AMERICAN SPANISH (español latino, NEUTRAL Mexican/Colombian accent)",
    "es-ES": "EUROPEAN SPANISH (Castilian)",
    "en": "NEUTRAL ENGLISH (American or international, NOT British)",
    "pt": "BRAZILIAN PORTUGUESE",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="user-config.json")
    ap.add_argument("--script", required=True, help="script.json with 6 scenes")
    ap.add_argument("--out", required=True, help="output directory for scene-{1..6}.mp4")
    ap.add_argument("--model", default=None,
                    choices=list(SUPPORTED_VIDEO_MODELS) + [None],
                    help="Override video model (kling3_0 or seedance_2_0). "
                         "If omitted, reads config.video_model.")
    ap.add_argument("--duration", type=int, default=5,
                    help="Seconds per scene (default 5)")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    script = json.loads(Path(args.script).read_text())

    model_uuid = config["modelo"]["uuid_higgsfield"]
    idioma_desc = IDIOMA_MAP.get(config["idioma"], IDIOMA_MAP["es-LATAM"])
    video_model = args.model or config.get("video_model", "kling3_0")
    if video_model == "ask-each-time":
        print("ERROR: video_model is 'ask-each-time' in config. Pass --model "
              "kling3_0 or --model seedance_2_0 explicitly.")
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(script['scenes'])} scenes sequentially with "
          f"{video_model} ({args.duration}s each)...\n", flush=True)
    results = []
    for s in script["scenes"]:
        n = s["n"]
        print(f"--- scene-{n} ---", flush=True)
        out_path = out_dir / f"scene-{n}.mp4"
        status, info = generate_scene(
            s, model_uuid, idioma_desc, out_path,
            video_model=video_model, duration=args.duration,
        )
        symbol = "✓" if status == "OK" else "✗"
        print(f"{symbol} scene-{n}: {info}\n", flush=True)
        results.append((n, status))
        time.sleep(8)

    ok = sum(1 for _, s in results if s == "OK")
    print(f"=== DONE: {ok}/{len(results)} OK ===")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
