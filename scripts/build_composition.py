#!/usr/bin/env python3
"""Construye composición HyperFrames a partir de 6 videos + transcripts.

Uso:
  python3 build_composition.py --config <user-config.json> --project <hyperframes-project-dir>

Lee scene-{1..6}.mp4 y transcript-scene-{1..6}.json del project-dir.
Aplica correcciones del glossary (universal + config.extra_corrections.captions).
Genera index.html sin transitions, hard cuts, captions sincronizados.
"""
import argparse
import json
import re
from pathlib import Path

# Universal corrections (Whisper errors common in Spanish LATAM)
UNIVERSAL_CORRECTIONS = {
    "Cloud": "Claude",
    "cloud": "Claude",
    "orizontes": "Horizontes",
    "Orizontes": "Horizontes",
    "Yhace": "Y hace",
    "videllos": "videos",
    "necesiteaba": "necesitaba",
    "sintiéndomos": "sintiéndome",
    "superpernida": "súper perdida",
}

SCENE_DURATION = 5.0
NUM_SCENES = 6
TOTAL_DURATION = SCENE_DURATION * NUM_SCENES  # 30s


def apply_corrections(words: list, corrections: dict) -> list:
    out = []
    for w in words:
        text = w["text"]
        clean = text.rstrip(",.!?¿¡")
        suffix = text[len(clean):]
        if clean in corrections:
            text = corrections[clean] + suffix
        out.append({"text": text, "start": w["start"], "end": w["end"]})
    return out


def group_words(words: list, scene_offset: float) -> list:
    groups = []
    current = []
    for w in words:
        current.append(w)
        is_last = w is words[-1]
        ends_phrase = bool(re.search(r"[.,!?]$", w["text"]))
        if is_last or (ends_phrase and len(current) >= 3) or len(current) >= 5:
            text = " ".join(x["text"] for x in current).strip()
            groups.append({
                "text": text,
                "start": current[0]["start"] + scene_offset,
                "end": current[-1]["end"] + scene_offset,
            })
            current = []
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--project", required=True, help="HyperFrames project dir")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    proj = Path(args.project)

    extra_caption_corrections = (
        config.get("extra_corrections", {}).get("captions", {})
    )
    corrections = {**UNIVERSAL_CORRECTIONS, **extra_caption_corrections}

    all_groups = []
    for i in range(1, NUM_SCENES + 1):
        transcript_path = proj / f"transcript-scene-{i}.json"
        if not transcript_path.exists():
            print(f"WARN: missing {transcript_path}")
            continue
        words = json.loads(transcript_path.read_text())
        words = apply_corrections(words, corrections)
        offset = (i - 1) * SCENE_DURATION
        all_groups.extend(group_words(words, offset))

    # Avoid track overlaps — small gap between consecutive caption groups
    for j in range(len(all_groups) - 1):
        if all_groups[j]["end"] >= all_groups[j + 1]["start"] - 0.02:
            all_groups[j]["end"] = all_groups[j + 1]["start"] - 0.02

    print(f"Generated {len(all_groups)} caption groups")
    for g in all_groups:
        print(f"  [{g['start']:.2f}-{g['end']:.2f}] {g['text']}")

    # Build HTML
    scene_html = "".join(
        f'\n    <video class="clip scene-video" id="v{i}" '
        f'data-start="{(i - 1) * SCENE_DURATION}" '
        f'data-duration="{SCENE_DURATION}" data-track-index="0" '
        f'src="scene-{i}.mp4" muted playsinline></video>'
        f'\n    <audio class="clip" id="a{i}" '
        f'data-start="{(i - 1) * SCENE_DURATION}" '
        f'data-duration="{SCENE_DURATION}" data-track-index="2" '
        f'src="scene-{i}.mp4" data-volume="1"></audio>'
        for i in range(1, NUM_SCENES + 1)
    )

    caption_html = "".join(
        f'\n    <div class="clip caption-group" id="cg-{idx}" '
        f'data-start="{g["start"]:.3f}" '
        f'data-duration="{max(g["end"] - g["start"], 0.5):.3f}" '
        f'data-track-index="1">{g["text"]}</div>'
        for idx, g in enumerate(all_groups)
    )

    groups_js = json.dumps([
        {"id": f"cg-{i}", "start": g["start"], "end": g["end"]}
        for i, g in enumerate(all_groups)
    ])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>UGC Ad — {config['negocio']['marca']}</title>
  <style>
    body {{ margin: 0; padding: 0; background: #000; }}
    #ad {{
      position: relative;
      background: #000;
      overflow: hidden;
    }}
    .scene-video {{
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      object-fit: cover;
    }}
    .caption-group {{
      position: absolute;
      bottom: 360px;
      left: 60px; right: 60px;
      text-align: center;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      font-weight: 800;
      font-size: 62px;
      line-height: 1.15;
      color: #ffffff;
      text-shadow:
        0 0 8px rgba(0,0,0,0.9),
        0 4px 20px rgba(0,0,0,0.85),
        0 2px 4px rgba(0,0,0,1);
      letter-spacing: -0.5px;
      opacity: 0;
      will-change: opacity, transform;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <div id="ad" data-composition-id="ad" data-start="0" data-duration="{TOTAL_DURATION}" data-width="1080" data-height="1920">{scene_html}{caption_html}

    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      const GROUPS = {groups_js};
      const SCENE_DURATION = {SCENE_DURATION};
      const NUM_SCENES = {NUM_SCENES};

      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});

      // Hard cuts — no fades. Each scene appears at full opacity.
      for (let i = 1; i <= NUM_SCENES; i++) {{
        tl.set("#v" + i, {{ opacity: 1 }}, (i - 1) * SCENE_DURATION);
      }}

      GROUPS.forEach(function (g, idx) {{
        const sel = "#" + g.id;
        tl.fromTo(sel,
          {{ opacity: 0, y: 24, scale: 0.92 }},
          {{ opacity: 1, y: 0, scale: 1, duration: 0.18, ease: "back.out(1.4)" }},
          g.start);
        tl.to(sel,
          {{ opacity: 0, y: -8, scale: 0.96, duration: 0.12, ease: "power2.in" }},
          g.end - 0.12);
        tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, g.end);
      }});

      window.__timelines["ad"] = tl;
    </script>
  </div>
</body>
</html>"""

    out = proj / "index.html"
    out.write_text(html)
    print(f"\n✓ Wrote {out}")
    print(f"Composition: 1080x1920, {TOTAL_DURATION}s, {len(all_groups)} caption groups")


if __name__ == "__main__":
    main()
