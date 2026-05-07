# Workflow — publicar anuncio a Meta Ads

Este flow corre **opcionalmente** después del paso 7 (render final), solo si `config.meta.enabled == true`.

## Pre-requisitos

- `config/user-config.json` existe con `meta.enabled: true`
- `meta` CLI autenticado (`meta auth status` devuelve OK)
- El MP4 final del anuncio existe en `<project-dir>/anuncio-final.mp4`

Si Meta CLI NO está disponible o no autenticado, **detener** y avisar al usuario:

> El Meta CLI no está autenticado. Sigue la guía para configurarlo:
> https://www.skool.com/horizontes-ia-9992/meta-ads-y-claude-acaba-de-cambiar-todo-nuevo-video

## Paso 0 — cargar config

```python
config = json.load(open("config/user-config.json"))
meta_config = config["meta"]  # ad_account_id, page_id, etc.
```

## Paso 1 — preguntar overrides para ESTE anuncio

Hacer mínimas preguntas (con defaults del config):

> Voy a crear el anuncio en tu cuenta Meta. Confirma o ajusta:
>
> - **URL destino**: `{config.cta.url_principal}` ¿correcto o quieres cambiar?
> - **Presupuesto diario**: `${meta_config.default_daily_budget_usd}` ¿OK o ajustar?
> - **Objetivo**: `{meta_config.default_objective}` ¿OK?
> - **Audiencia**: defaults LATAM (`{countries}`, `{age_min}-{age_max}`) ¿OK o custom?

Capturar overrides en dict `ad_overrides`.

## Paso 2 — Generar nombre de campaña

Patrón: `[TEST] {marca} - {tema-slug} - {YYYY-MM-DD}`

Ejemplo: `[TEST] Horizontes IA - comunidad-skool - 2026-05-07`

**REGLA CRÍTICA**: el prefijo `[TEST]` es obligatorio mientras el skill esté generando ads automáticos. Esto evita confundir tests con producción y permite filtros fáciles en Ads Manager.

## Paso 3 — Ejecutar publish_to_meta.py

```bash
python3 scripts/publish_to_meta.py \
  --config config/user-config.json \
  --video <project-dir>/anuncio-final.mp4 \
  --campaign-name "[TEST] Marca - tema - 2026-05-07" \
  --tema "comunidad-skool" \
  --url "https://miweb.com/landing" \
  --daily-budget 10 \
  --objective OUTCOME_LEADS
```

El script:
1. Sube el MP4 a Meta como video creative (`meta videos upload`)
2. Crea la campaña en `PAUSED` con el nombre construido
3. Crea el ad set con audiencia + presupuesto + targeting
4. Crea el ad linking creative + ad set
5. Marca `is_ai_powered: true` en el creative (Meta AI disclosure 2024+)
6. Devuelve los IDs creados

## Paso 4 — Reportar al usuario

```
✅ Anuncio subido a Meta en estado PAUSED:

  Campaign: [TEST] {marca} - {tema} - {fecha}
  Campaign ID: 12024XXXXXXXXX
  Ad Set ID: 12024YYYYYYYYY
  Ad ID: 12024ZZZZZZZZZ
  Creative ID: 12024CCCCCCCCC

📋 URL del Ads Manager:
  https://adsmanager.facebook.com/adsmanager/manage/ads?act={ad_account_id}&selected_campaign_ids={campaign_id}

⚠️ ANTES de activar:
  1. Abre el ad en Ads Manager y revisa el preview
  2. Verifica que el AI disclosure esté marcado (campo "Made with AI")
  3. Confirma la URL destino y la audiencia
  4. Activa cuando estés listo (cambia status PAUSED → ACTIVE)

⏱️ Meta tarda 1-24h en aprobar el creative (especialmente con AI-generated).
   Si rechazan, te llega notificación con el motivo.
```

## Paso 5 — opcional: A/B test

Si el usuario tiene 2 anuncios (A y B) y quiere A/B test:

> ¿Quieres crear un segundo ad set en la misma campaña para A/B test del otro video?

Si SÍ, repetir paso 3 con el segundo video, agregando `--ad-set-only` al comando para reusar la campaña.

## Manejo de errores

- **Token expirado**: `meta auth login` y reintentar
- **Insufficient permissions**: el ad account no tiene permisos para crear campañas — pedir al usuario que verifique en Business Manager
- **Video rejected**: Meta a veces rechaza videos por problemas técnicos (codec, resolución). El skill ya genera 1080×1920 H.264 que es compatible — si pasa, reportar el error específico
- **Budget too low**: Meta tiene mínimos por país/objetivo. Subir o cambiar audiencia

## Disclaimer

Este skill **nunca** activa anuncios automáticamente. Siempre los deja en `PAUSED`. La activación es manual desde Ads Manager para que el usuario tenga control total y revise antes de gastar dinero.
