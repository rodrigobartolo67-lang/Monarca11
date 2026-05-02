from flask import Blueprint, current_app, jsonify, render_template, request
from werkzeug.utils import secure_filename

from web.services.translation import translate_text

main_bp = Blueprint("main", __name__)


def _allowed_file(filename: str) -> bool:
    allowed = current_app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@main_bp.post("/translate")
def translate_file():
    if "file" not in request.files:
        return jsonify({"error": "No se encontró archivo."}), 400

    uploaded_file = request.files["file"]
    target_language = request.form.get("target_language", "español")

    if uploaded_file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío."}), 400

    if not _allowed_file(uploaded_file.filename):
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

    safe_name = secure_filename(uploaded_file.filename)
    file_path = current_app.config["UPLOAD_FOLDER"] / safe_name
    uploaded_file.save(file_path)

    try:
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        translated = translate_text(text, target_language)
    finally:
        if file_path.exists():
            file_path.unlink()

    return jsonify({
        "filename": safe_name,
        "target_language": target_language,
        "translated_text": translated,
    })
