#!/usr/bin/env python3
"""Publica un anuncio UGC ya renderizado a Meta Ads en estado PAUSED.

Uso:
  python3 publish_to_meta.py \
    --config config/user-config.json \
    --video <path-to-mp4> \
    --campaign-name "[TEST] Marca - tema - YYYY-MM-DD" \
    --tema "tema-slug" \
    --url "https://destino.com" \
    --daily-budget 10 \
    --objective OUTCOME_LEADS

Crea: campaña → ad set → ad creative → ad. Todo en PAUSED.
Marca is_ai_powered=True en el creative para AI disclosure de Meta.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_meta(args: list, capture: bool = True):
    """Ejecuta el meta CLI y devuelve el JSON parseado."""
    cmd = ["meta"] + args + ["--output", "json"]
    print(f"  $ {' '.join(cmd)}", file=sys.stderr)
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if r.returncode != 0:
        print(f"  ERROR: {r.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout) if capture and r.stdout.strip() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--video", required=True, help="Path al MP4 final del anuncio")
    ap.add_argument("--campaign-name", required=True)
    ap.add_argument("--tema", required=True)
    ap.add_argument("--url", required=True, help="URL destino del ad")
    ap.add_argument("--daily-budget", type=float, required=True, help="USD por día")
    ap.add_argument("--objective", default="OUTCOME_LEADS",
                    choices=["OUTCOME_LEADS", "OUTCOME_TRAFFIC",
                             "OUTCOME_SALES", "OUTCOME_ENGAGEMENT"])
    ap.add_argument("--message", default=None,
                    help="Texto principal del ad (sobre el video). "
                         "Si no se especifica, se genera desde config")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text())
    if not config.get("meta", {}).get("enabled"):
        print("ERROR: config.meta.enabled is false. Run setup wizard or edit config.")
        sys.exit(1)

    meta_cfg = config["meta"]
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"ERROR: video not found: {video_path}")
        sys.exit(1)

    ad_account_id = meta_cfg["ad_account_id"]
    page_id = meta_cfg["page_id"]
    audience = meta_cfg["default_audience"]

    print(f"=== Publicando a Meta — ad account {ad_account_id} ===\n")

    # Paso 1 — subir video como creative
    print("1. Subiendo video a Meta...")
    video = run_meta([
        "videos", "upload",
        "--account-id", ad_account_id,
        "--file", str(video_path),
        "--name", f"UGC-{args.tema}",
    ])
    video_id = video["id"]
    print(f"   ✓ Video ID: {video_id}\n")

    # Paso 2 — crear campaña en PAUSED
    print("2. Creando campaña...")
    daily_budget_cents = int(args.daily_budget * 100)
    campaign = run_meta([
        "campaigns", "create",
        "--account-id", ad_account_id,
        "--name", args.campaign_name,
        "--objective", args.objective,
        "--status", "PAUSED",
        "--special-ad-categories", "NONE",
    ])
    campaign_id = campaign["id"]
    print(f"   ✓ Campaign ID: {campaign_id}\n")

    # Paso 3 — crear ad set
    print("3. Creando ad set...")
    ad_set_targeting = {
        "geo_locations": {"countries": audience.get("countries", ["MX"])},
        "age_min": audience.get("age_min", 25),
        "age_max": audience.get("age_max", 45),
    }
    if "languages" in audience:
        ad_set_targeting["locales"] = audience["languages"]

    ad_set_args = [
        "adsets", "create",
        "--account-id", ad_account_id,
        "--campaign-id", campaign_id,
        "--name", f"{args.campaign_name} — Ad Set 1",
        "--daily-budget", str(daily_budget_cents),
        "--billing-event", "IMPRESSIONS",
        "--optimization-goal",
        ("LEAD_GENERATION" if args.objective == "OUTCOME_LEADS"
         else "LINK_CLICKS"),
        "--targeting", json.dumps(ad_set_targeting),
        "--status", "PAUSED",
    ]
    if meta_cfg.get("pixel_id"):
        ad_set_args += ["--pixel-id", meta_cfg["pixel_id"]]
    ad_set = run_meta(ad_set_args)
    ad_set_id = ad_set["id"]
    print(f"   ✓ Ad Set ID: {ad_set_id}\n")

    # Paso 4 — crear ad creative con AI disclosure
    print("4. Creando ad creative (con AI disclosure)...")
    message = args.message or (
        f"{config['negocio']['marca']} — {config['cta']['accion_deseada']}"
    )
    creative = run_meta([
        "creatives", "create",
        "--account-id", ad_account_id,
        "--name", f"UGC Creative — {args.tema}",
        "--page-id", page_id,
        "--video-id", video_id,
        "--link", args.url,
        "--message", message,
        "--call-to-action", "LEARN_MORE",
        "--is-ai-powered", "true",  # Meta AI disclosure 2024+
    ])
    creative_id = creative["id"]
    print(f"   ✓ Creative ID: {creative_id}\n")

    # Paso 5 — crear ad
    print("5. Creando ad...")
    ad = run_meta([
        "ads", "create",
        "--account-id", ad_account_id,
        "--ad-set-id", ad_set_id,
        "--creative-id", creative_id,
        "--name", f"UGC Ad — {args.tema}",
        "--status", "PAUSED",
    ])
    ad_id = ad["id"]
    print(f"   ✓ Ad ID: {ad_id}\n")

    print("=" * 60)
    print("✅ TODO EN PAUSED — listo para revisar")
    print("=" * 60)
    print(f"\nCampaign:  {campaign_id}")
    print(f"Ad Set:    {ad_set_id}")
    print(f"Creative:  {creative_id}")
    print(f"Ad:        {ad_id}")
    print(f"Video:     {video_id}\n")
    acct_clean = ad_account_id.replace("act_", "")
    print(f"📋 Abrir en Ads Manager:")
    print(f"   https://adsmanager.facebook.com/adsmanager/manage/ads?"
          f"act={acct_clean}&selected_campaign_ids={campaign_id}")
    print(f"\n⚠️  ANTES de activar:")
    print(f"   1. Revisa el preview en Ads Manager")
    print(f"   2. Verifica el AI disclosure ('Made with AI')")
    print(f"   3. Confirma URL y audiencia")
    print(f"   4. Cambia status PAUSED → ACTIVE manualmente cuando estés listo")
    print(f"\n⏱️  Meta tarda 1-24h en aprobar el creative.")


if __name__ == "__main__":
    main()
