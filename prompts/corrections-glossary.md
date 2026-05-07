# Glossary fonético — dialogue ↔ caption

Mapping de palabras que el modelo de lip-sync (Kling 3.0) NO pronuncia bien si las escribes en su forma normal escrita. La columna izquierda es lo que escribes en el `dialogue` que va al prompt de Kling. La columna derecha es lo que el caption visual debe mostrar (post-corrección al transcript de Whisper).

## Tabla universal (siempre aplica, español LATAM)

| Concepto | Dialogue (fonético, lo que va al prompt) | Caption visual (corrige Whisper) |
|---|---|---|
| Punto en URL | `punto com` / `punto co` / `punto net` | `.com` / `.co` / `.net` |
| Inteligencia Artificial (sigla) | `i a` (con espacio) | `IA` |
| API (sigla) | `a p i` | `API` |
| URL (sigla) | `u r l` | `URL` |
| OK | `okey` | `OK` |
| @ (arroba) | `arroba` | `@` |
| & | `y` | `&` |
| 0.5 | `cero punto cinco` | `0.5` |
| %  | `por ciento` | `%` |
| Claude (Anthropic) | `Klaud` | `Claude` |
| ChatGPT | `chat g p t` | `ChatGPT` |
| GitHub | `Guit jab` | `GitHub` |
| YouTube | `Yutub` | `YouTube` |
| Skool | `skool` (suena igual, pero a veces sale "school" — escribir `skool`) | `Skool` |
| Notion | `Noushon` | `Notion` |
| Slack | `Sláck` (acento ayuda a no decir "slec") | `Slack` |

## Whisper auto-corrections (errores comunes en transcripción)

Whisper a veces transcribe mal el español LATAM. Aplicar siempre estos reemplazos en el caption:

| Whisper escribe | Reemplazar por |
|---|---|
| `Cloud` | `Claude` |
| `cloud` | `Claude` |
| `orizontes` | `Horizontes` |
| `Orizontes` | `Horizontes` |
| `Yhace` (palabras unidas) | `Y hace` |
| `videllos` | `videos` |
| `necesiteaba` | `necesitaba` |
| `sintiéndomos` | `sintiéndome` |
| `superpernida` | `súper perdida` |
| `nim` (cuando contexto sugiere "sin saber") | `sin saber` |

## Sufijos preservados

Cuando reemplaces una palabra, preserva su signo de puntuación:
- `Cloud,` → `Claude,`
- `Cloud.` → `Claude.`

## Para añadir al config del usuario

Si el usuario tiene su propia marca con palabras raras, agregar a `config.extra_corrections`:

```json
{
  "extra_corrections": {
    "phonetic": {
      "MiMarca SaaS": "Mi Marca Sas",
      "AmazonAWS": "amazon a w s"
    },
    "captions": {
      "Mi Marca Sas": "MiMarca SaaS",
      "amazon a w s": "AmazonAWS"
    }
  }
}
```

## Algoritmo de aplicación

**Al generar dialogue** (antes de mandar al prompt de Kling):
1. Tomar el guion natural del LLM (con palabras escritas normales)
2. Para cada entry en glossary universal + `config.extra_corrections.phonetic`: reemplazar
3. Resultado = dialogue fonético que va al prompt

**Al generar caption** (después de transcribir con Whisper):
1. Tomar el JSON de Whisper (palabras + timestamps)
2. Para cada palabra: si está en glossary universal o en `config.extra_corrections.captions`: reemplazar texto
3. Mantener timestamps originales
4. Group en chunks de 3-5 palabras → caption final

## Edge cases

- **Casing**: matchear case-insensitive pero preservar capitalización inicial si el match era capitalizado
- **Múltiples palabras**: para reemplazos multi-word (`a p i` → `API`), buscar la sequencia exacta de tokens en el array de Whisper (varios words consecutivos con el texto)
- **Palabras con sufijo** (`Cloud,` o `Cloud.`): strip puntuación, match, re-añadir
