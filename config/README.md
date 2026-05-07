# Config

Este directorio contiene `user-config.json` — la personalización del usuario, generada en setup.

**NO está en git** (incluido en `.gitignore`) porque cada usuario tiene su propia config.

Si nunca corriste el setup, el archivo no existe — el skill lo detecta y arranca el wizard.

Para regenerar el setup:

```bash
rm config/user-config.json
# luego activa el skill — disparará el wizard
```

## Estructura

```json
{
  "version": 1,
  "created_at": "2026-05-07T...",
  "negocio": {
    "marca": "Mi Marca",
    "que_vende": "Comunidad de IA en español",
    "icp": "Profesionales 25-45 LATAM"
  },
  "cta": {
    "url_principal": "miweb.com",
    "como_encontrar": "buscan Mi Marca en Skool",
    "accion_deseada": "entrar a la comunidad"
  },
  "modelo": {
    "tipo": "pool",
    "imagen_path": "pool/modelo-04-mujer-tech-late20s.png",
    "uuid_higgsfield": "abc-123-...",
    "descripcion": "Hispanic late 20s, glasses, hoodie"
  },
  "tono_default": "natural-recien-despertada",
  "setting_default": "mixto",
  "idioma": "es-LATAM",
  "extra_corrections": {
    "phonetic": {
      "Mi Marca": "mi marca"
    },
    "captions": {
      "mi marca": "Mi Marca"
    }
  }
}
```
