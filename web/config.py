import tempfile
from pathlib import Path


class Config:
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # 1 GB
    UPLOAD_FOLDER = Path(tempfile.gettempdir()) / "monarca_uploads"
    ALLOWED_EXTENSIONS = {
        "txt", "md", "rtf", "doc", "docx", "pdf", "html", "json", "xml", "csv",
        "py", "js", "ts", "java", "c", "cpp", "cs"
    }
