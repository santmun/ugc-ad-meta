# Template — prompt para Kling 3.0 (lip-sync)

Este es el template fijo del prompt que se manda a Kling 3.0 para cada escena. Sustituir `{dialogue}`, `{vibe}`, `{extra}`, `{idioma}` con valores reales antes de mandar.

## Template

```
The person speaks this {idioma} dialogue with perfect lip-sync, reading the text EXACTLY as written (every word, every space):

"{dialogue}"

CRITICAL RULES:

(1) Spoken language must be {idioma_descripcion}. NOT European Spanish from Spain.
    No "vosotros" form. No Castilian "z/c" lisp.

(2) Read the dialogue PHONETICALLY as written. Do NOT translate any word into English equivalents.
    If "punto com" → say "punto com" (NOT "dot com").
    If "i a" → say two separate Spanish letters (NOT "ya").
    If "Klaud" → say it like English "cloud" (rhymes with "loud"), this is the brand "Claude".
    If "app" → say like English "app" (one short syllable).
    Do NOT invent extra syllables.

(3) Vibe: {vibe}.

(4) {extra}

(5) Articulation: clear pronunciation, every syllable distinct.
    For two-word combinations with same starting consonant
    (sin saber, más simple, etc.), articulate the words SEPARATELY,
    do NOT slur them together.

(6) Performance: maintain natural eye contact with the camera lens.
    Subtle natural head movements that match the speech cadence.
    NO theatrical or forced gestures.
    NO bringing hands to the face.
    Realistic everyday selfie behavior.

(7) Closing tone: at the end of the sentence, the tone should rise/stay UP
    (not flat-falling) — this prepares a smooth transition to the next clip.

(8) Visual continuity: background, hair, outfit must remain visually IDENTICAL
    to the start frame. Do NOT modify her/his hair shape, length, or style.

Selfie-recording UGC vibe, vertical 9:16 format.
```

## Cómo llenar `{idioma}` y `{idioma_descripcion}`

| `config.idioma` | `{idioma}` | `{idioma_descripcion}` |
|---|---|---|
| `es-LATAM` | `Spanish` | `LATIN AMERICAN SPANISH (español latino, NEUTRAL Mexican/Colombian accent)` |
| `es-ES` | `Spanish` | `EUROPEAN SPANISH (Castilian)` |
| `en` | `English` | `NEUTRAL ENGLISH (American or international, NOT British)` |
| `pt` | `Portuguese` | `BRAZILIAN PORTUGUESE` |

## Cómo llenar `{vibe}` por escena

| Escena | Vibe sugerido (ajustar a `config.tono_default`) |
|---|---|
| 1 Hook | "warm, intimate, casual just-woke-up vibe, slightly soft voice" |
| 2 Tensión | "slightly overwhelmed but engaged, expressive sigh, sincere" |
| 3 Pivote | "relieved discovery, genuine smile starting, confidential tone" |
| 4 Resultado general | "satisfied confident, slightly more energetic, animated" |
| 5 Valor concreto | "ENERGETIC excited, slightly bouncy, like sharing a discovery" |
| 6 CTA | "warm casual recommendation, direct eye contact, friendly invitation" |

Si `config.tono_default = enérgico`, sumar "more energetic" a todos.
Si `config.tono_default = storytelling`, sumar "reflective slow pacing" a 1-3 y "calm satisfied" a 4-6.

## Cómo llenar `{extra}` (opcional, por escena)

Solo si la escena tiene un detalle particular. Ejemplos:

- Hook caminando: `"Subtle natural walking camera movement, no excessive head shaking. She walks slowly while talking."`
- Escena con marca rara: `"When she says 'NombreMarca' she pronounces it as 'fonético equivalente'."`
- Escena con setting custom: `"She is in {setting}, lighting is {lighting}."`

Si no aplica nada, dejar `{extra}` vacío.

## Comando completo (referencia)

```bash
higgsfield generate create kling3_0 \
  --prompt "<output del template arriba>" \
  --aspect_ratio "9:16" \
  --duration 5 \
  --image <UUID_modelo_o_imagen_base> \
  --wait --json
```

## Costo

- Kling 3.0 9:16 5s con imagen: ~9 créditos reales por video
- 6 escenas: ~54 créditos por anuncio
- + 0 créditos imagen base (se reutiliza UUID configurado)

## Tips de retry

Kling devuelve **HTTP 502** ocasionalmente (rate limit cuando se manda > 1 job en paralelo). Siempre correr secuencial con sleep 8s entre cada uno. Si falla, retry con backoff (30s, 60s).

Si después de 3 retries sigue fallando, marcar el video como ERROR y avisar al usuario para regenerar individual al final.
