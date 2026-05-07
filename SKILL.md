---
name: ugc-ad-meta
description: Genera anuncios UGC (User Generated Content) para Meta Ads desde un brief en lenguaje natural. Crea persona realista hablando a cámara con lip-sync, audio nativo en español LATAM, captions sincronizados y render final 1080×1920 listo para subir a Meta. Primera vez instalado, ejecuta setup wizard que personaliza el skill al negocio del usuario (CTA, marca, modelo de persona, tono).
triggers:
  - "haz un anuncio para meta"
  - "crea un ad ugc"
  - "anuncio meta ugc"
  - "genera un anuncio para mi negocio"
  - "hacer un reel/anuncio para instagram/meta"
  - "ad para facebook/instagram"
  - "lánzame un creative ugc"
---

# ugc-ad-meta

Skill genérico para generar anuncios UGC en Meta Ads. Una persona realista habla a cámara como si grabara con su celular, en formato vertical 9:16, con lip-sync en español LATAM y subtítulos sincronizados.

## Filosofía

> **Si nunca te ejecutaron antes, primero corre el setup wizard. Si ya estás configurado, lee `config/user-config.json` y pide solo el TEMA del anuncio. Aplica todas las reglas fonéticas y de tono automáticamente sin que el usuario tenga que recordarlas.**

El usuario solo dice **qué quiere comunicar**. El skill se encarga de:
- Generar guion conversacional natural (no "tienes que ver esto" estilo influencer)
- Pronunciación fonética automática (`Klaud`, `skool punto com`, `i a`, etc.)
- Lip-sync con Kling 3.0
- Composición HyperFrames + captions con post-corrección
- Render final 1080×1920 MP4 listo para Meta

---

## Workflow

### Detección de primera ejecución

Lee `config/user-config.json`. Si NO existe, ejecuta `workflow/00-first-time-setup.md` (entrevista al usuario, genera config). Si SÍ existe, salta directo al paso 1 abajo.

### 1. Recolectar TEMA del anuncio

Cargar `prompts/interview-ad.md` y hacer **mínimas** preguntas:

- ¿De qué quieres que hable este anuncio? (tu producto, una promo, un beneficio específico)
- ¿Algún ángulo emocional? (descubrimiento, alivio, FOMO, social proof) — opcional, default = config.tono_default

Todo lo demás (CTA, modelo, tono, idioma) viene del config.

### 2. Generar guion (6 escenas × 5s = 30s)

Cargar `workflow/02-script-rules.md`. Estructura **siempre** la misma:

| # | Beat | Función |
|---|---|---|
| 1 | Hook | Capturar atención conversacional |
| 2 | Tensión | Identificar el problema |
| 3 | Pivote | "Hasta que descubrí..." |
| 4 | Resultado general | Beneficio amplio |
| 5 | Valor concreto | Caso real / outcome específico |
| 6 | CTA | Llamada a acción soft |

Aplicar **automáticamente** el glossary de `prompts/corrections-glossary.md` para escribir dialogue fonéticamente.

### 3. Pausa de approval

Mostrar el guion completo en tabla. Esperar OK del usuario antes de gastar créditos en Kling. Esta pausa es OBLIGATORIA — los videos cuestan ~9 cr c/u y regenerar 6 = ~54 cr.

### 4. Generar 6 videos con Kling 3.0

Ejecutar `scripts/generate_ad.py` que usa el template de `prompts/video-lipsync-template.md`. SIEMPRE secuencial (no paralelo) con backoff — Kling tiene rate limits agresivos.

Para cada video:
- aspect_ratio: 9:16
- duration: 5
- image: UUID del modelo configurado en config
- prompt: template con dialogue fonético + reglas LATAM + vibe configurado

### 5. Pausa de revisión visual

Pedir al usuario que abra los 6 MP4 individualmente y verifique:
- Lip-sync de cada palabra
- Pronunciación correcta de marca / URL
- Gestos no exagerados
- Sin objetos raros (manos en cara, etc.)

Si alguna falla, regenerar individual antes de seguir.

### 6. Componer + transcribir + corregir captions

Ejecutar `scripts/transcribe_correct.py`:
- Transcribir cada video con Whisper español
- Aplicar corrections del glossary (`Klaud → Claude`, `skool punto com → skool.com`, etc.)
- Generar HTML HyperFrames con captions sincronizados (sin transitions, hard cuts)

### 7. Render final

```bash
cd <project-dir> && npx hyperframes render -o anuncio-final.mp4
```

Reportar path del MP4 + tamaño + duración.

### 8. (Opcional) Publish a Meta Ads — solo si `config.meta.enabled == true`

Si en el setup el usuario eligió configurar Meta también, ejecutar `workflow/06-publish-meta.md`:

1. Cargar `config.meta` (page_id, ad_account_id, audience defaults, presupuesto)
2. Preguntar overrides para ESTE anuncio (URL destino, presupuesto diario, objetivo)
3. Ejecutar `scripts/publish_to_meta.py` que crea:
   - Campaña en estado `PAUSED` con prefijo `[TEST]`
   - Ad set con audiencia configurada
   - Ad creative con el MP4 + flag `is_ai_powered: true` (AI disclosure de Meta)
4. Reportar IDs creados y URL al ad en Meta Ads Manager
5. Recordar al usuario: revisar y activar manualmente desde Ads Manager

Si `config.meta.enabled == false`, **saltar este paso** y reportar al usuario:
> Tu anuncio está listo. Súbelo manualmente a Meta Ads Manager cuando quieras.

---

## Reglas críticas (NUNCA romper)

1. **Idioma audio**: solo español LATAM (config.idioma) — nunca dejar que Kling use español de España o inglés
2. **Dialogue fonético**: escribir EXACTAMENTE como debe sonar (`punto com` no `.com`, `i a` no `IA`, `Klaud` no `Claude`)
3. **Captions visuales**: usan forma normal (`.com`, `IA`, `Claude`) vía post-procesamiento del transcript
4. **Sin transitions**: hard cuts entre escenas, no crossfades (más natural UGC)
5. **6 escenas × 5s**: estándar — no improvisar duración
6. **Tono natural**: filler words ("bueno", "o sea", "te juro") — NO "tienes que ver esto" influencer
7. **Compliance Meta**: no claims financieros garantizados, no targeting por atributos personales, disclosure de AI requerido al subir

---

## Archivos del skill

- `config/user-config.json` — generado en setup, contiene marca/CTA/modelo del usuario
- `workflow/00-first-time-setup.md` — entrevista de instalación
- `workflow/02-script-rules.md` — reglas de redacción del guion
- `prompts/interview-ad.md` — preguntas mínimas por anuncio
- `prompts/video-lipsync-template.md` — template del prompt Kling
- `prompts/corrections-glossary.md` — fonético ↔ caption mapping
- `scripts/setup_wizard.py` — auto-configuración inicial
- `scripts/generate_ad.py` — orquestador end-to-end
- `scripts/transcribe_correct.py` — Whisper + correcciones
- `scripts/build_composition.py` — HyperFrames builder
- `scripts/publish_to_meta.py` — opcional, sube a Meta Ads en PAUSED
- `workflow/06-publish-meta.md` — flujo de publicación a Meta
- `pool/` — 6 modelos starter (mujeres latinas) que el usuario puede usar tal cual
- `examples/anuncio-demo.mp4` — anuncio de referencia

---

## Dependencias

**Obligatorias** (para generar anuncios):
- `higgsfield` CLI (`npm install -g @higgsfield/cli` + `higgsfield auth login`) — para Kling 3.0 + GPT Image 2
- `hyperframes` CLI (vía `npx hyperframes`) — para composición + render
- Python 3.10+ con `subprocess`, `urllib`, `json` (todos stdlib)
- `jq` (para parsing CLI output)
- `ffmpeg` (lo instala HyperFrames si falta)

**Opcional** (solo si vas a publicar a Meta desde el skill):
- `meta-ads` CLI (`pip install meta-ads` o `uv tool install meta-ads`) — para subir directo a Meta Ads
- Credenciales Meta configuradas (access token, ad account ID, page ID)
- Si NO sabes cómo instalar Meta CLI o configurarlo, hay guía completa aquí:
  **https://www.skool.com/horizontes-ia-9992/meta-ads-y-claude-acaba-de-cambiar-todo-nuevo-video**
