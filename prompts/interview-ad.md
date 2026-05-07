# Entrevista — preguntas mínimas por anuncio

Cuando el usuario ya tiene `config/user-config.json` (skill ya configurado), solo necesitas extraer el TEMA del anuncio. Mínima fricción.

## Pregunta 1 — obligatoria

> **¿De qué quieres que sea este anuncio?**

Espera respuesta libre del usuario. Ejemplos:
- "De mi nuevo curso de SEO"
- "Para promocionar mi promo del Black Friday"
- "Quiero atraer gente a mi comunidad de marketing"

## Pregunta 2 — opcional (solo si la respuesta no implica un ángulo claro)

> **¿Quieres un ángulo emocional específico?**
> - **Descubrimiento**: "encontré algo que me cambió"
> - **Alivio**: "ya no estoy perdida"
> - **FOMO**: "todos están haciendo esto menos tú"
> - **Social proof**: "yo ya logré X gracias a Y"
> - **Curiosidad**: "no me lo van a creer"

Si el usuario dice "tú decides", aplicar el `config.tono_default`.

## Pregunta 3 — opcional (si quiere variar)

> **¿Algo específico que mencionar?** (un beneficio, un caso real, un número)

## NO preguntar (ya está en config)

❌ Modelo de la persona — viene de `config.modelo`
❌ CTA / URL — viene de `config.cta`
❌ Idioma — viene de `config.idioma`
❌ Tono general — viene de `config.tono_default`
❌ Setting visual — viene de `config.setting_default`

Si el usuario quiere cambiar alguno de estos PARA UN ANUNCIO ESPECÍFICO, lo expresa directamente: "este quiero que sea más enérgico" — entonces overrride solo para ese.

## Output de la entrevista

Estructurar como dict en memoria:

```python
ad_brief = {
    "tema": "...",
    "angulo": "descubrimiento" | "alivio" | "fomo" | "social-proof" | "curiosidad" | None,
    "extras": "..." | None,
    "overrides": {
        # solo si el usuario pidió cambiar algo del config
        "tono": "...",
        "setting": "...",
    }
}
```

Pasar este dict al generador del guion (`workflow/02-script-rules.md`).
