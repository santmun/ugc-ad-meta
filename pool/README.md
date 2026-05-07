# Pool de modelos starter

6 mujeres latinas pre-generadas con GPT Image 2 (9:16 1k high). Listas para usar como base de cualquier anuncio UGC. **Cada usuario configura cuál usa en `config/user-config.json`.**

| # | Archivo | Descripción | Vibe sugerido |
|---|---|---|---|
| 1 | `modelo-01-mujer-casual-20s.png` | Latina early 20s, suéter beige, fondo cocina con plantas | Casual, cercano |
| 2 | `modelo-02-mujer-profesional-mid20s.png` | Latina mid 20s, blusa blanca, sala minimalista | Profesional, limpio |
| 3 | `modelo-03-mujer-creator-30s.png` | Latina early 30s, cardigan, home-office con libros | Creator establecida |
| 4 | `modelo-04-mujer-tech-late20s.png` | Hispanic late 20s, lentes + hoodie, escritorio tech | Tech-savvy, dev |
| 5 | `modelo-05-mujer-natural-mid20s.png` | Latina mid 20s, blusa blanca, solarium con plantas | Wellness, natural |
| 6 | `modelo-06-mujer-mama-pro-30s.png` | Latina early 30s, suéter rosa, cocina mañanera | Mom-pro, cercano |

## Cómo usar

El setup wizard te muestra estas 6 opciones y te deja escoger una. La que elijas se sube a Higgsfield UNA vez (obtiene UUID) y se reutiliza en todos tus anuncios.

## Generar tu propio modelo (custom)

Si ninguno encaja con tu marca, durante setup eliges "custom" y el skill te hace 4 sub-preguntas (género, edad, look, etnia) y genera 6 nuevas opciones para ti con GPT Image 2 (~24 créditos).

## Roadmap

- [ ] Hombres (currently 0 male models)
- [ ] Edades 40s+
- [ ] Distintas etnias (afro, asiática, anglo)
- [ ] Distintos settings (gym, café, parque, oficina)

Pull requests welcome para añadir modelos al pool.
