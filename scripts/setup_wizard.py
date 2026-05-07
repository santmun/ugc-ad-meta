#!/usr/bin/env python3
"""Setup wizard interactivo — corre la primera vez para personalizar el skill.

Uso:
  python3 setup_wizard.py --out config/user-config.json

Este script guía al usuario por las 12 preguntas del setup. NO está diseñado para
correr autónomo en un agent loop — es interactivo. Para uso en agent, el AGENT
debe hacer las preguntas naturalmente (ver workflow/00-first-time-setup.md) y
construir el JSON manualmente con los mismos campos.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


POOL_DESCRIPTIONS = {
    "modelo-01-mujer-casual-20s.png": "Latina early 20s, casual, suéter beige, plantas",
    "modelo-02-mujer-profesional-mid20s.png": "Latina mid 20s, blusa blanca, sala minimalista",
    "modelo-03-mujer-creator-30s.png": "Latina early 30s, cardigan, home-office con libros",
    "modelo-04-mujer-tech-late20s.png": "Hispanic late 20s, lentes + hoodie, escritorio tech",
    "modelo-05-mujer-natural-mid20s.png": "Latina mid 20s, blusa blanca, solarium plantas",
    "modelo-06-mujer-mama-pro-30s.png": "Latina early 30s, suéter rosa, cocina mañanera",
}


def ask(question: str, options: list = None, default: str = None) -> str:
    print(f"\n{question}")
    if options:
        for i, opt in enumerate(options, 1):
            mark = " (default)" if default and opt.startswith(default) else ""
            print(f"  {i}. {opt}{mark}")
    if default:
        print(f"  [Enter para usar default: {default}]")
    answer = input("> ").strip()
    if not answer and default:
        return default
    if options and answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(options):
            return options[idx]
    return answer


def check_dependencies():
    print("=== Verificando dependencias ===\n")
    checks = [
        ("higgsfield", "npm install -g @higgsfield/cli"),
        ("npx", "instalar Node.js desde https://nodejs.org"),
        ("ffmpeg", "brew install ffmpeg  (o equivalente en tu OS)"),
    ]
    missing = []
    for cmd, fix in checks:
        ok = subprocess.run(["which", cmd], capture_output=True).returncode == 0
        print(f"  {'✓' if ok else '✗'} {cmd}")
        if not ok:
            missing.append((cmd, fix))
    if missing:
        print("\nFALTAN dependencias:")
        for cmd, fix in missing:
            print(f"  - {cmd}: {fix}")
        sys.exit(1)
    auth = subprocess.run(["higgsfield", "account", "status"],
                          capture_output=True, text=True)
    if "@" not in auth.stdout:
        print("\n✗ Higgsfield no autenticado.")
        print("  Corre: higgsfield auth login")
        sys.exit(1)
    print(f"\n✓ Higgsfield: {auth.stdout.strip()}\n")


def upload_image(path: Path) -> str:
    r = subprocess.run(["higgsfield", "upload", "create", str(path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"upload failed: {r.stderr}")
    return r.stdout.strip().split("\n")[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="config/user-config.json")
    ap.add_argument("--pool-dir", default="pool")
    args = ap.parse_args()

    check_dependencies()

    print("=" * 60)
    print(" SETUP UGC AD META — primera configuración")
    print("=" * 60)

    # === Bloque 1: negocio ===
    marca = ask("1. ¿Cómo se llama tu marca/negocio?")
    que_vende = ask("2. ¿Qué vendes/ofreces? (una frase)")
    icp = ask("3. ¿Quién es tu cliente ideal?")

    # === Bloque 2: CTA ===
    url_principal = ask("4. ¿Cuál es tu URL principal? (ej: tudominio.com)")
    como_encontrar = ask("5. ¿Cómo te encuentran? (ej: 'buscan X en Y' o URL)")
    accion = ask("6. ¿Qué quieres que la gente haga? "
                 "(ej: 'entrar a la comunidad')")

    # === Bloque 3: modelo ===
    modelo_tipo = ask(
        "7. ¿Modelo del anuncio?",
        options=["pool (incluido, 0 cr)", "custom (genera, ~24 cr)"],
        default="pool"
    )
    if modelo_tipo.startswith("pool"):
        print("\nModelos disponibles en el pool:")
        pool_dir = Path(args.pool_dir)
        files = sorted(pool_dir.glob("modelo-*.png"))
        for i, f in enumerate(files, 1):
            desc = POOL_DESCRIPTIONS.get(f.name, "")
            print(f"  {i}. {f.name} — {desc}")
        choice = int(input("\nElige número del modelo > ").strip())
        modelo_path = files[choice - 1]
    else:
        print("Custom model NO implementado en wizard interactivo.")
        print("Usa el agent para generar — ver workflow/00-first-time-setup.md")
        sys.exit(1)

    print(f"\nSubiendo {modelo_path.name} a Higgsfield para reutilizar...")
    modelo_uuid = upload_image(modelo_path)
    print(f"UUID: {modelo_uuid}")

    # === Bloque 4: tono y setting ===
    tono = ask("8. ¿Qué tono prefieres?",
               options=["cercano", "natural-recien-despertada",
                        "storytelling", "energico"],
               default="natural-recien-despertada")

    setting = ask("9. ¿Setting visual default?",
                  options=["caminando-outdoor", "casa-sofa",
                           "escritorio-laptop", "mixto"],
                  default="mixto")

    # === Bloque 5: idioma ===
    idioma = ask("10. ¿Idioma del anuncio?",
                 options=["es-LATAM", "es-ES", "en", "pt"],
                 default="es-LATAM")

    # === Bloque 6: extra corrections ===
    extra_in = input(
        "\n11. ¿Tu marca tiene palabras técnicas/siglas/URLs que pronunciar?\n"
        "   Formato: palabra1=fonético1,palabra2=fonético2  (Enter para skip)\n"
        "   Ej: Skool.com=skool punto com,API=a p i\n> "
    ).strip()
    phonetic = {}
    captions = {}
    if extra_in:
        for pair in extra_in.split(","):
            if "=" in pair:
                k, v = pair.split("=", 1)
                phonetic[k.strip()] = v.strip()
                captions[v.strip()] = k.strip()

    # === Bloque 7: compliance ===
    print("\n12. Aviso Meta: cuando subas el anuncio en Meta Ads Manager")
    print("    DEBES marcar 'AI-generated content' en el ad form (regla 2024+).")
    input("    [Enter para confirmar que entendiste]")

    config = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "negocio": {
            "marca": marca,
            "que_vende": que_vende,
            "icp": icp,
        },
        "cta": {
            "url_principal": url_principal,
            "como_encontrar": como_encontrar,
            "accion_deseada": accion,
        },
        "modelo": {
            "tipo": modelo_tipo.split()[0],
            "imagen_path": str(modelo_path),
            "uuid_higgsfield": modelo_uuid,
            "descripcion": POOL_DESCRIPTIONS.get(modelo_path.name, ""),
        },
        "tono_default": tono,
        "setting_default": setting,
        "idioma": idioma,
        "extra_corrections": {
            "phonetic": phonetic,
            "captions": captions,
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"\n✓ Setup completo. Config guardado en {out}")
    print("\nPara crear tu primer anuncio, dime al agent: 'haz un anuncio sobre X'")


if __name__ == "__main__":
    main()
