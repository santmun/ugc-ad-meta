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
