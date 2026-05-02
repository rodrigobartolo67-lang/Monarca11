# Traductor legal de archivos (estructura web)

Aplicación web en Flask con estructura modular para subir archivos y traducir su contenido jurídico.

## Estructura

```text
web/
  __init__.py          # factory create_app
  config.py            # configuración global
  routes.py            # endpoints HTTP
  services/
    translation.py     # integración de traducción
  templates/
    index.html
  static/
    style.css
run.py                 # punto de entrada
```

## Características

- Carga de archivos hasta **1 GB**.
- Validación de extensiones permitidas.
- Procesamiento temporal en disco para archivos pesados.
- Endpoints: `/`, `/health`, `/translate`.
- Traducción con OpenAI (`OPENAI_API_KEY`) y modo demo si no hay clave.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Abrir: `http://localhost:8000`

## Recomendado para producción

1. Cola de tareas asíncronas (Celery/RQ).
2. Almacenamiento externo (S3/Blob).
3. OCR para PDFs escaneados.
4. Auditoría, cifrado y control de acceso.
5. Revisión humana para traducción legal final.
