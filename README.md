# ugc-ad-meta

Skill de Claude Code para generar anuncios UGC (User Generated Content) para Meta Ads desde un brief en lenguaje natural.

Una persona realista habla a cámara como si grabara con su celular, en formato vertical 9:16, con lip-sync en español LATAM y subtítulos sincronizados. **Listo para subir a Facebook/Instagram Ads Manager**.

## Demo

Ver `examples/anuncio-demo.mp4` para ver el output esperado (30s, 1080×1920, 6 escenas, audio nativo en español, captions sincronizados).

## Cómo funciona

1. **Primera vez** que activas el skill, te entrevisto con 12 preguntas para personalizar:
   - Tu marca / negocio / ICP
   - Tu CTA / URL
   - Modelo de la persona (pool incluido o custom)
   - Tono default + setting visual
   - Idioma + correcciones fonéticas custom

   Esto genera `config/user-config.json` que el skill usa después.

2. **Para cada anuncio** después, solo dices:
   > *"haz un anuncio de mi nuevo curso"*

   El skill:
   - Genera 6 escenas de guion conversacional natural
   - Aplica reglas fonéticas automáticas (`skool.com → skool punto com`, `Claude → Klaud`, etc.)
   - Pide approval del guion
   - Genera 6 videos con Kling 3.0 (lip-sync nativo, audio español LATAM)
   - Compone con HyperFrames + captions sincronizados (sin transitions, hard cuts)
   - Renderiza MP4 final 1080×1920

**Costo por anuncio**: ~54 créditos Higgsfield (≈ $1-2 USD según plan).

## Stack

- **Higgsfield Kling 3.0** — image-to-video con lip-sync + audio nativo
- **Higgsfield GPT Image 2** — generación de imagen base de la persona (solo en setup custom)
- **HyperFrames** — composición HTML → MP4 con captions sincronizados
- **Whisper (small, español)** — transcripción para generar captions

## Instalación

### 1. Instalar como skill de Claude Code

```bash
cd ~/.claude/skills/
git clone https://github.com/santmun/ugc-ad-meta.git
```

(o usar `npx skills add santmun/ugc-ad-meta` cuando tu agent lo soporte)

### 2. Instalar CLIs requeridos

```bash
# Higgsfield
npm install -g @higgsfield/cli
higgsfield auth login

# HyperFrames (vía npx, no requiere install global)
npx hyperframes doctor   # verifica deps
```

### 3. Activar el skill

En Claude Code, di:

> "haz un anuncio para meta"

La primera vez correrá el setup wizard. Después solo te pide el TEMA.

## Estructura del repo

```
ugc-ad-meta/
├── SKILL.md                       # Entry point para el agent
├── README.md                      # Este archivo
├── config/
│   └── user-config.json           # Auto-generado en setup
├── workflow/
│   ├── 00-first-time-setup.md
│   ├── 02-script-rules.md
│   └── ...
├── prompts/
│   ├── interview-ad.md
│   ├── video-lipsync-template.md
│   └── corrections-glossary.md
├── scripts/
│   ├── setup_wizard.py
│   ├── generate_ad.py
│   ├── transcribe_correct.py
│   └── build_composition.py
├── pool/                          # 6 modelos starter (mujeres latinas)
└── examples/
    └── anuncio-demo.mp4
```

## Filosofía

**Genérico**: el skill no asume ningún negocio en particular. Cada usuario configura su marca/CTA/modelo en setup. Pueden ser desde una academia, una tienda Shopify, un SaaS, un consultor — lo que sea.

**Setup-once**: la primera vez es interrogatorio. Después es 1 frase para crear cada anuncio.

**Natural sobre clickbait**: el guion sigue reglas anti-influencer (sin "tienes que ver esto", sin promesas garantizadas). Suena como una persona real recomendando algo a una amiga.

**Phonetic-aware**: el dialogue se escribe EXACTAMENTE como debe sonar (`skool punto com` no `.com`, `Klaud` no `Claude`). Los captions visuales se corrigen después con un glossary post-procesamiento.

## Compliance Meta (MUY importante)

Cuando subas el anuncio a Meta Ads Manager, DEBES marcar **"AI-generated content"** en el ad form. Es regla de Meta desde 2024. El skill te lo recuerda al final.

Otras reglas que el skill respeta:
- No claims financieros garantizados
- No targeting por atributos personales
- No clickbait engañoso
- Disclosure de AI obligatorio

## Limitaciones conocidas

- Kling 3.0 ocasionalmente devuelve **HTTP 502** si recibes muchos jobs en paralelo. El skill SIEMPRE corre secuencial con backoff.
- El audio español de Kling es bueno pero NO perfecto. Para palabras críticas (marca, CTA), las reglas fonéticas las arreglan, pero verifica antes de publicar.
- Whisper a veces transcribe mal. El skill aplica un glossary de correcciones automáticas, pero si tu marca es muy rara, agrégala a `extra_corrections` en el config.

## Roadmap (sugerencias)

- [ ] Soporte multi-idioma (en, pt) — actualmente español LATAM solo
- [ ] Generación de variantes A/B (diferentes hooks para test)
- [ ] Integración directa con Meta Ads CLI para upload automático
- [ ] Pool ampliado de modelos (hombres, distintas etnias, distintas edades)

## Licencia

MIT
