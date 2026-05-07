# Setup Wizard — Primera vez

Este flow corre UNA vez, cuando `config/user-config.json` no existe. Entrevista al usuario y genera el archivo de configuración personalizado.

## Antes de empezar — verificar dependencias

Ejecutar checks:

```bash
which higgsfield || echo "FALTA: npm install -g @higgsfield/cli"
higgsfield account status 2>&1 | grep -q "@" || echo "FALTA: higgsfield auth login"
which npx || echo "FALTA: instalar Node.js"
which ffmpeg || npx hyperframes doctor 2>&1
```

Si falta alguno: bloquear setup y guiar al usuario a instalar antes de continuar.

## Entrevista — 12 preguntas

Hacer una por una, breve y conversacional. NO un cuestionario de 12 a la vez. Acumular respuestas en memoria conforme avanza.

### Bloque 1 — Negocio

1. **¿Cómo se llama tu marca/negocio?** (ej: "Horizontes IA", "Mi Tienda")
2. **¿Qué vendes/ofreces? Una frase.** (ej: "comunidad de IA en español para profesionales LATAM")
3. **¿Quién es tu cliente ideal?** (ej: "profesionales 25-45 en CDMX que quieren aprender IA")

### Bloque 2 — CTA (call to action)

4. **¿Cuál es tu URL principal? O ¿cómo te encuentran?**
   Opciones:
   - URL directa: `tudominio.com`
   - Búsqueda en plataforma: "buscan X en Y" (ej: "buscan Horizontes en Skool")
   - DM en redes: "manda DM a @cuenta"
5. **¿Qué quieres que la gente haga después de ver el anuncio?** (ej: "entrar a la comunidad", "agendar demo", "comprar curso")

### Bloque 3 — Modelo (la persona del anuncio)

6. **¿Quieres usar uno de los modelos del pool incluido o generar uno custom?**
   - **Pool**: 6 mujeres latinas en distintos vibes (casual, profesional, tech, natural, mom-pro, creator). Listas para usar — 0 créditos extra.
   - **Custom**: el skill genera 6 opciones de modelo según tus criterios (gasta ~24 créditos).

   Si elige **custom**, preguntar:
   - 6a. Género: hombre / mujer / cualquiera
   - 6b. Rango de edad: 20s / 30s / 40s+
   - 6c. Look: casual / profesional / tech / wellness / mom-pro / creator
   - 6d. Etnia / región: latina, mestiza, afro, asiática, anglo, multi (default = "latina")

   Generar las 6 imágenes con `gpt_image_2` 9:16 1k high y mostrar para escoger.

7. **¿Cuál de los modelos eliges?** (mostrar 6 con paths, número 1-6)

### Bloque 4 — Tono y estilo

8. **¿Qué tono prefieres para los anuncios?**
   - **Cercano**: "oigan les quiero contar" — íntimo, conversacional
   - **Natural recién despertada**: "bueno, acabo de despertarme" — UGC más auténtico, menos planeado
   - **Storytelling**: "hace meses estaba perdida..." — reflexivo, personal
   - **Enérgico**: "tienen que ver esto" — urgencia, hype

9. **¿Dónde se filma típicamente?** (define el setting visual default)
   - Caminando outdoor (selfie en la calle)
   - En casa / sofá (cozy)
   - Escritorio con laptop (work setting)
   - Mixto (varía por escena)

### Bloque 5 — Idioma

10. **¿Idioma del anuncio?**
    - español-LATAM (default — todo el glossary fonético configurado)
    - español-España (requiere ajustar prompts)
    - inglés
    - portugués

11. **¿Tu marca tiene palabras técnicas / siglas / URLs raras que pronunciar?**
    Ej: "Skool.com" → "skool punto com", "AI" → "a i", "@usuario" → "arroba usuario"
    Capturar como `extra_corrections` en el config.

### Bloque 6 — Compliance

12. **Aviso Meta**: te recuerdo que cuando subas el anuncio en Meta Ads Manager debes marcar "AI-generated content" en el ad form (regla Meta 2024+). Confirmar que lo entendiste. ✓

### Bloque 7 — Modelo de generación de video

13. **¿Qué modelo de generación de video prefieres usar como default?**

    Hay 2 opciones, cada uno tiene sus pros:

    - **`kling3_0` (Kling 3.0)** — RECOMENDADO para empezar
       - ~9 créditos por video → ~54 cr por anuncio
       - Mejor lip-sync, audio claro
       - Mejor cuando dialogue tiene siglas/marcas raras (i a, Klaud)
       - ⚠️ Rate-limit estricto, debe correr secuencial (devuelve HTTP 502 si paralelo)

    - **`seedance_2_0` (Seedance 2.0)**
       - ~22-27 créditos por video → ~135-162 cr por anuncio
       - Audio más natural, más cinematic
       - Mejor para tono storytelling / reflexivo
       - Más caro (3x), úsalo cuando la calidad importa más que el costo

    - **`ask-each-time`** — el skill te pregunta antes de cada anuncio cuál usar

    Si no estás seguro, elige `kling3_0` (default recomendado).

### Bloque 8 — Publicación a Meta (opcional)

14. **¿Quieres también poder publicar los anuncios directo a Meta desde aquí?**

    Opciones:
    - **Sí, configurar Meta también**: instalo y configuro el Meta Ads CLI. Después de cada anuncio podrás decir "súbelo a Meta" y queda en estado PAUSED listo para revisar y publicar manualmente.
    - **No, solo generar los videos**: el skill solo te entrega el MP4. Tú lo subes manualmente a Meta Ads Manager. (Setup más rápido, sin dependencias extra.)

    ---

    **Si responde "Sí, configurar Meta"**:

    14a. **¿Ya tienes el Meta Ads CLI instalado y autenticado?** (comando: `meta`, instalado vía `pip install meta-ads`)
       - Verificar con: `which meta && meta auth status`

       Si NO lo tiene instalado o no sabe qué es, **detener este bloque y mostrar al usuario**:

       > El Meta Ads CLI necesita instalación + token de Meta + permisos de tu Business Manager. La guía paso-a-paso completa está aquí:
       >
       > **https://www.skool.com/horizontes-ia-9992/meta-ads-y-claude-acaba-de-cambiar-todo-nuevo-video**
       >
       > Una vez que termines la instalación de allí, vuelve y corre el setup otra vez. Mientras tanto, configuro el skill SOLO para generar (puedes activar Meta después editando `config/user-config.json`).

       Setear `config.meta.enabled = false` y continuar con el setup.

    14b. (Solo si Meta CLI está instalado) **Recolectar IDs**:
       - Ad Account ID (`act_...`) — `meta accounts list`
       - Page ID (la página de Facebook que aparece como anunciante) — `meta pages list`
       - Default Pixel ID (opcional) — para tracking
       - Default presupuesto diario USD (ej: 10)
       - Default objetivo de campaña: `OUTCOME_LEADS` / `OUTCOME_TRAFFIC` / `OUTCOME_SALES` / `OUTCOME_ENGAGEMENT`
       - Default audiencia: usar la del config principal (LATAM 25-45) o custom (preguntar)

    14c. Verificar permisos:
       ```bash
       meta accounts info <ad_account_id>
       ```
       Si devuelve error → mostrar mensaje y enlazar al post de Skool.

    Si todo OK → setear `config.meta.enabled = true` y guardar IDs.

### Bloque 9 — Output config (incluye video_model + meta)

Agregar a config:

```json
{
  ...
  "video_model": "kling3_0",
  ...
}
```

Valores válidos: `"kling3_0"`, `"seedance_2_0"`, `"ask-each-time"`.

### Output config.meta (continuación)

Si meta enabled, agregar al user-config.json:

```json
{
  "meta": {
    "enabled": true,
    "ad_account_id": "act_...",
    "page_id": "...",
    "pixel_id": "..." | null,
    "default_objective": "OUTCOME_LEADS",
    "default_daily_budget_usd": 10,
    "default_audience": {
      "countries": ["MX", "CO", "AR", "PE", "CL"],
      "age_min": 25,
      "age_max": 45,
      "languages": ["spa"]
    }
  }
}
```

Si NO enabled:

```json
{
  "meta": {
    "enabled": false,
    "_note": "Para activar, instala Meta CLI siguiendo https://www.skool.com/horizontes-ia-9992/meta-ads-y-claude-acaba-de-cambiar-todo-nuevo-video y luego edita este config a enabled:true con los IDs."
  }
}
```

## Generar `config/user-config.json`

```json
{
  "version": 1,
  "created_at": "<ISO-date>",
  "negocio": {
    "marca": "...",
    "que_vende": "...",
    "icp": "..."
  },
  "cta": {
    "url_principal": "...",
    "como_encontrar": "...",
    "accion_deseada": "..."
  },
  "modelo": {
    "tipo": "pool" | "custom",
    "imagen_path": "pool/modelo-04-mujer-tech-late20s.png",
    "uuid_higgsfield": "<uploaded once, reused for all ads>",
    "descripcion": "Hispanic woman late 20s, glasses, dark hoodie"
  },
  "tono_default": "natural-recien-despertada",
  "setting_default": "caminando-outdoor",
  "idioma": "es-LATAM",
  "extra_corrections": {
    "phonetic": {
      "skool.com": "skool punto com",
      "Horizontes IA": "Horizontes"
    },
    "captions": {
      "skool punto com": "skool.com",
      "orizontes": "Horizontes"
    }
  }
}
```

## Subir la imagen del modelo a Higgsfield

```bash
UUID=$(higgsfield upload create <imagen_path> | tail -1)
```

Guardar `UUID` en `config.modelo.uuid_higgsfield` para reutilizar en todos los anuncios sin re-subir.

## Confirmar setup completo

Mostrar resumen tabular del config y decir:

> Setup listo. Para crear tu primer anuncio, dime de qué quieres que sea.

Ejemplo: *"haz un anuncio de mi nueva clase gratis"* → arranca el workflow normal.
