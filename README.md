# Traductor legal de archivos (base)

Proyecto base para subir archivos y traducir su contenido.

## Qué incluye

- Interfaz web básica para subir archivos.
- Endpoint backend con `multer` para manejar carga de archivos grandes (hasta 1 GB configurado).
- Respuesta de traducción simulada (debes conectar un proveedor real para producción).

## Ejecutar

```bash
npm install
npm start
```

Luego abre: `http://localhost:3000`

## Recomendaciones para producción legal

1. Integrar un motor de traducción robusto (DeepL, Azure Translator, Google Cloud Translation o modelo on-premise).
2. Cifrar archivos en tránsito y en reposo.
3. Registrar trazabilidad de cambios por auditoría.
4. Implementar cola de procesamiento para documentos muy pesados.
5. Añadir OCR para PDFs escaneados y DOCX parser.
