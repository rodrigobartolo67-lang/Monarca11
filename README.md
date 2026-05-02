# Traductor legal de archivos (base)

Aplicación web básica para subir archivos y traducir su contenido, pensada para documentos jurídicos extensos.

## Características

- Subida de archivos con límite de hasta **1 GB** (`MAX_CONTENT_LENGTH`).
- Tipos de archivo permitidos para texto/código comunes.
- Procesamiento temporal en disco (evita cargar todo en memoria desde frontend).
- Endpoint de salud (`/health`).
- Integración con OpenAI vía `OPENAI_API_KEY`.
- Modo demo sin clave API.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abrir: `http://localhost:8000`

## Nota importante para producción

Para documentos legales críticos y archivos muy pesados, se recomienda:

1. Cola de tareas (Celery/RQ) para procesamiento asíncrono.
2. Almacenamiento externo (S3/Blob) en vez de disco local.
3. OCR para PDFs escaneados.
4. Control de versiones de traducción y revisión humana.
5. Cifrado de archivos y auditoría de acceso.
