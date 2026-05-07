#!/usr/bin/env python3
"""Health check del entorno antes de generar anuncios.

Uso:
  python3 scripts/doctor.py [--config config/user-config.json]

Verifica:
- higgsfield CLI instalado + autenticado + saldo suficiente
- npx hyperframes funciona
- ffmpeg disponible
- Si --config dado, valida campos obligatorios
- Si config.meta.enabled, verifica meta CLI
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def ok(msg):
    print(f"  {GREEN}✓{RESET} {msg}")


def fail(msg):
    print(f"  {RED}✗{RESET} {msg}")


def warn(msg):
    print(f"  {YELLOW}⚠{RESET}  {msg}")


def check_cmd(cmd: str, install_hint: str) -> bool:
    r = subprocess.run(["which", cmd], capture_output=True, text=True)
    if r.returncode == 0:
        ok(f"{cmd} disponible: {r.stdout.strip()}")
        return True
    fail(f"{cmd} no encontrado. Install: {install_hint}")
    return False


def check_higgsfield():
    print("\n[1] Higgsfield CLI")
    if not check_cmd("higgsfield", "npm install -g @higgsfield/cli"):
        return False

    r = subprocess.run(["higgsfield", "account", "status"],
                       capture_output=True, text=True)
    if r.returncode != 0 or "@" not in r.stdout:
        fail("higgsfield no autenticado. Corre: higgsfield auth login")
        return False

    line = r.stdout.strip()
    ok(f"autenticado: {line}")

    # Extraer créditos
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*credits", line)
    if m:
        credits = float(m.group(1).replace(",", ""))
        if credits < 60:
            warn(f"saldo bajo ({credits} cr). Recomendado: ≥60 cr "
                 "(1 anuncio Kling = ~54 cr, 1 anuncio Seedance = ~135 cr)")
        elif credits < 200:
            ok(f"{credits} cr — alcanza para ~{int(credits / 54)} anuncios Kling")
        else:
            ok(f"{credits} cr — saldo amplio")
    return True


def check_hyperframes():
    print("\n[2] HyperFrames")
    if not check_cmd("npx", "instalar Node.js desde https://nodejs.org"):
        return False
    r = subprocess.run(["npx", "hyperframes", "--version"],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        fail(f"npx hyperframes falló: {r.stderr[:200]}")
        return False
    ok(f"hyperframes: {r.stdout.strip()}")
    return True


def check_ffmpeg():
    print("\n[3] ffmpeg")
    return check_cmd("ffmpeg", "brew install ffmpeg (macOS) o apt install ffmpeg (Linux)")


def check_jq():
    print("\n[4] jq")
    return check_cmd("jq", "brew install jq (macOS) o apt install jq (Linux)")


def check_config(path: Path) -> bool:
    print("\n[5] Config del usuario")
    if not path.exists():
        warn(f"{path} no existe. El skill arrancará setup wizard al activarse.")
        return True  # not a hard failure

    try:
        cfg = json.loads(path.read_text())
    except Exception as e:
        fail(f"config inválido: {e}")
        return False

    required = ["negocio", "cta", "modelo", "tono_default", "idioma"]
    missing = [k for k in required if k not in cfg]
    if missing:
        fail(f"faltan campos obligatorios: {missing}")
        return False
    ok("campos obligatorios OK")

    # Validate modelo.uuid_higgsfield
    if not cfg["modelo"].get("uuid_higgsfield"):
        fail("modelo.uuid_higgsfield vacío. Re-corre setup.")
        return False
    ok(f"modelo: {cfg['modelo'].get('descripcion', 'sin descripción')}")

    # Validate video_model
    vm = cfg.get("video_model", "kling3_0")
    if vm not in ("kling3_0", "seedance_2_0", "ask-each-time"):
        warn(f"video_model='{vm}' no reconocido (esperado kling3_0/seedance_2_0/ask-each-time)")
    else:
        ok(f"video_model: {vm}")

    # Meta optional
    meta = cfg.get("meta", {})
    if meta.get("enabled"):
        print("\n[5b] Meta Ads (config.meta.enabled = true)")
        if not check_cmd("meta", "pip install meta-ads"):
            return False
        if not meta.get("ad_account_id") or not meta.get("page_id"):
            fail("config.meta falta ad_account_id o page_id")
            return False
        ok(f"ad_account_id: {meta['ad_account_id']}")
        ok(f"page_id: {meta['page_id']}")
        # Try a soft auth check
        r = subprocess.run(["meta", "auth", "status"],
                           capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            warn(f"meta auth status falló: {r.stderr[:200]}")
        else:
            ok("meta CLI autenticado")
    else:
        ok("Meta deshabilitado (modo solo-generar)")

    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/user-config.json")
    args = ap.parse_args()

    print("=" * 60)
    print(" UGC AD META — health check")
    print("=" * 60)

    results = [
        check_higgsfield(),
        check_hyperframes(),
        check_ffmpeg(),
        check_jq(),
        check_config(Path(args.config)),
    ]

    print("\n" + "=" * 60)
    if all(results):
        print(f" {GREEN}✓ TODO OK — listo para generar anuncios{RESET}")
        print("=" * 60)
        return 0
    else:
        print(f" {RED}✗ Hay problemas — revisa arriba antes de continuar{RESET}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
