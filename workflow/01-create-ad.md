# Workflow — crear un anuncio

Este flow corre cuando `config/user-config.json` ya existe (skill ya configurado).

## Paso 0 — cargar config

```python
config = json.load(open("config/user-config.json"))
```

Verificar que tiene todos los campos requeridos. Si falta algo crítico, sugerir re-correr setup.

## Paso 1 — Entrevista mínima

Cargar `prompts/interview-ad.md` y hacer las preguntas (1 obligatoria, 2-3 opcionales).

## Paso 2 — Generar guion (6 escenas)

Cargar `workflow/02-script-rules.md` y aplicar.

Output: 6 dialogues escritos fonéticamente (`skool punto com`, `i a`, `Klaud`, etc.) + vibe por escena.

## Paso 3 — Mostrar guion al usuario y pedir OK

Tabla:

| # | Beat | Dialogue (fonético) | Vibe |
|---|---|---|---|
| 1 | Hook | ... | warm casual |
| 2 | Tensión | ... | overwhelmed |
| ... | ... | ... | ... |

Avisar costo: **~54 créditos** (6 videos × ~9 cr).

Esperar OK explícito antes de gastar.

## Paso 4 — Crear directorio del proyecto

```bash
PROJ=~/ugc-ads-output/{marca-slug}-{YYYY-MM-DD}-{tema-slug}
mkdir -p "$PROJ"
```

## Paso 5 — Generar 6 videos con Kling 3.0

Guardar el guion como `script.json`:

```json
{
  "scenes": [
    {"n": 1, "dialogue": "...", "vibe": "...", "extra": ""},
    ...
  ]
}
```

Correr:

```bash
python3 scripts/generate_ad.py \
  --config config/user-config.json \
  --script $PROJ/script.json \
  --out $PROJ
```

El script corre secuencial con backoff. Toma ~5 minutos para los 6.

## Paso 6 — Pausa de revisión visual

Pedir al usuario:

> Verifica los 6 videos abriéndolos:
>
> ```bash
> open $PROJ/scene-1.mp4
> ```
>
> Confirma:
> 1. Lip-sync de cada palabra
> 2. Pronunciación correcta de marca / URL
> 3. Gestos no exagerados
> 4. Sin objetos raros (manos en cara)
>
> ¿Todas OK o regenero alguna?

Si una escena necesita regenerar, volver al paso 5 solo para esa escena (modificar vibe / dialogue / image base).

## Paso 7 — Inicializar HyperFrames + transcribir

```bash
cd $PROJ
npx hyperframes init . --example blank --non-interactive --skip-transcribe --skip-skills
python3 scripts/transcribe_correct.py --project $PROJ
```

## Paso 8 — Construir composición

```bash
python3 scripts/build_composition.py \
  --config config/user-config.json \
  --project $PROJ
```

Genera `$PROJ/index.html` sin transitions, captions sincronizados, glossary aplicado.

## Paso 9 — Lint

```bash
cd $PROJ && npx hyperframes lint
```

Si hay errores, fix antes de renderizar. Warnings sobre `timeline_track_too_dense` se pueden ignorar.

## Paso 10 — Render

```bash
cd $PROJ && npx hyperframes render -o anuncio-final.mp4
```

Toma ~30s. Output: `$PROJ/anuncio-final.mp4` (~25-30 MB, 1080×1920).

## Paso 11 — Reportar al usuario

```
✅ Anuncio listo:
   Path: $PROJ/anuncio-final.mp4
   Tamaño: XX MB · 30s · 1080×1920
   Costo: ~XX créditos Higgsfield
   Saldo restante: XX cr

⚠️ Recuerda al subir a Meta Ads Manager:
   Marcar "AI-generated content" en el ad form (regla Meta 2024+).
```

## Pasos opcionales

### Regenerar UNA escena

Si después de revisar el render final, una escena no quedó bien:

1. Mover el video viejo: `mv $PROJ/scene-N.mp4 $PROJ/scene-N.OLD.mp4`
2. Ajustar dialogue / vibe en `script.json` solo para esa escena
3. Re-correr `generate_ad.py` (el script salta los que ya existen) — o ejecutar manualmente:
   ```bash
   higgsfield generate create kling3_0 --prompt "..." --image $UUID --aspect_ratio 9:16 --duration 5 --wait --json
   ```
4. Re-transcribir solo esa escena: `python3 scripts/transcribe_correct.py --project $PROJ` (sobrescribe)
5. Re-build + re-render

### Crear variantes A/B

Para test, generar 2 anuncios con guiones distintos pero misma estructura:
- Anuncio A: tono "cercano"
- Anuncio B: tono "energético"

Mismo modelo, mismo CTA. Cambiar solo `tono` en el override del entrevista.
