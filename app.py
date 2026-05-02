import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

try:
    from openai import OpenAI
except Exception:  # dependency may be optional during local setup
    OpenAI = None


UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "monarca_uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "txt", "md", "rtf", "doc", "docx", "pdf", "html", "json", "xml", "csv", "py", "js", "ts", "java", "c", "cpp", "cs"
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def translate_text(text: str, target_language: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return (
            "[MODO DEMO] Traducción no ejecutada porque falta OPENAI_API_KEY o la librería openai.\n\n"
            f"Destino solicitado: {target_language}\n\n"
            "Contenido original:\n"
            + text[:4000]
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Eres un traductor jurídico experto. Mantén numeración, citas y formato legal.",
            },
            {
                "role": "user",
                "content": f"Traduce al idioma: {target_language}. Texto:\n\n{text[:30000]}",
            },
        ],
    )
    return response.output_text


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/translate", methods=["POST"])
def translate_file():
    if "file" not in request.files:
        return jsonify({"error": "No se encontró archivo."}), 400

    uploaded_file = request.files["file"]
    target_language = request.form.get("target_language", "español")

    if uploaded_file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío."}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

    safe_name = secure_filename(uploaded_file.filename)
    file_path = UPLOAD_FOLDER / safe_name
    uploaded_file.save(file_path)

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        translated = translate_text(text, target_language)
    finally:
        if file_path.exists():
            file_path.unlink()

    return jsonify(
        {
            "filename": safe_name,
            "target_language": target_language,
            "translated_text": translated,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
