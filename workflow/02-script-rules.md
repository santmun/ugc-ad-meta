# Reglas de redacción del guion

## Estructura fija — 6 escenas × 5s = 30s total

| # | Beat | Función | Ejemplo (tono natural) |
|---|---|---|---|
| 1 | **Hook** | Capturar atención conversacional, no clickbait | "Bueno, acabo de despertarme y tenía que contarles esto..." |
| 2 | **Tensión** | Identificar el problema/dolor | "Llevo semanas sintiéndome súper perdida con todo lo de la i a..." |
| 3 | **Pivote** | "Hasta que descubrí..." | "Y hace poquito encontré una comunidad que me cambió toda la cabeza." |
| 4 | **Resultado general** | Beneficio amplio | "Ahora aprendo de gente que de verdad está construyendo cosas." |
| 5 | **Valor concreto** | Caso real / outcome específico | "Yo ya hice mi propia app con Klaud, te juro que sí." |
| 6 | **CTA** | Llamada a acción soft, conversational | "Si quieren checar, está en skool punto com, buscan {marca}." |

## Largo por escena

- **5 segundos** ≈ **14-17 palabras** en español hablado naturalmente
- Si una escena queda < 12 palabras: alargar con muletilla natural ("en serio", "te juro", "fíjate")
- Si queda > 18 palabras: cortar — el modelo va a hablar muy rápido y el lip-sync se rompe

## Tono — anti-influencer

✅ **Hacer**:
- Filler words: "bueno", "o sea", "te juro", "en serio", "fíjate", "neta"
- Frases cortas, oración por oración
- Lenguaje hablado, no escrito
- Sonar como recién despertada / amiga que te cuenta algo
- Pausas naturales entre ideas

❌ **Evitar**:
- "Tienes que ver esto" (suena influencer fake)
- "No te lo puedes perder" (cliché)
- "Te va a sorprender" (clickbait)
- Promesas absolutas ("vas a ganar", "te garantizo")
- Frases pulidas tipo coach ("transforma tu vida", "cambia el chip")
- Listas formales ("número uno, número dos")

## Transición entre escenas

Cada escena debe **terminar con tono UP** (no caer) para preparar la siguiente. Forma de lograrlo:

- Frase incompleta que continúa: "...y lo que pasó después es que..."
- Curiosidad implícita: "...te juro que sí" (deja al viewer queriendo más)
- Énfasis en la última palabra: "...sí se puede"

NO terminar cada escena con punto final flat. Mantener el viewer en estado de "qué sigue".

## Reglas fonéticas — el dialogue se escribe como suena

Aplicar SIEMPRE el glossary de `prompts/corrections-glossary.md`. Resumen:

| Palabra/expresión | Dialogue (cómo se escribe en el prompt) | Caption visual final |
|---|---|---|
| `.com` | `punto com` | `.com` |
| `IA` | `i a` (con espacio) | `IA` |
| `Claude` | `Klaud` | `Claude` |
| `API` | `a p i` | `API` |
| `URL` | `u r l` | `URL` |
| `@` | `arroba` | `@` |
| `&` | `y` | `&` |
| `0.5` | `cero punto cinco` | `0.5` |

Si la marca del usuario tiene palabras raras, agregarlas a `config.extra_corrections`.

## Palabras a EVITAR si es posible

Estas palabras dieron problemas en lip-sync con Kling 3.0:
- "necesitaba" → modelo dijo "necesitabia" — usar "tenía que" en su lugar
- "completamente" → muy larga, puede colapsar — usar "toda" / "todo"
- "construir" → ocasionalmente sale raro — usar "hacer" o "armar"
- "aplicación" → 4 sílabas, el modelo a veces atropella — usar "app"

## Palabras compuestas / juntas — peligrosas

Cuando dos palabras consecutivas comparten consonante similar, el modelo puede colapsarlas:
- "sin saber" → puede sonar "nim" — usar "y antes no sabía" en su lugar
- "más simple" → puede sonar "másimple" — usar "fácil"

**Regla**: si una escena crítica tiene 2 palabras seguidas con la misma consonante (S, R, N, T), reformular o agregar pausa con coma entre ellas.

## Ejemplo de aplicación

**Brief del usuario**: *"Quiero un anuncio para mi comunidad de marketing donde la gente aprende SEO."*

**Guion generado** (aplicando todo lo de arriba):

| # | Dialogue (fonético) | Caption (visual) |
|---|---|---|
| 1 | Bueno, acabo de despertarme y tenía que contarles algo, en serio. | "Bueno, acabo de despertarme y tenía que contarles algo, en serio." |
| 2 | Llevo meses queriendo crecer mi negocio con s e o pero no sabía por dónde empezar. | "Llevo meses queriendo crecer mi negocio con SEO pero no sabía por dónde empezar." |
| 3 | Y hace poquito encontré una comunidad que me cambió todo. | (igual) |
| 4 | Ahora aprendo de gente que ya rankea sus sitios en Google de verdad. | (igual) |
| 5 | Yo ya posicioné mi propia tienda en primera página, te juro. | (igual) |
| 6 | Si quieren checar, está en {url config.cta.como_encontrar}. | (con corrección post: skool punto com → skool.com) |

## Validación final del guion (antes de mostrar al usuario)

Checklist mental:
- [ ] 6 escenas
- [ ] 14-17 palabras por escena
- [ ] Sin "tienes que", "no te lo puedes perder", "te va a sorprender"
- [ ] Glossary fonético aplicado en marcas/URLs/siglas
- [ ] CTA en escena 6 referencia el `config.cta`
- [ ] Cada escena termina con tono que invita a la siguiente
