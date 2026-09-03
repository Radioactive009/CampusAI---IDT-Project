from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Files that should NOT be indexed
EXCLUDED_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "vector_store",
}

# Repository file types we want the RAG to understand
ALLOWED_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".json",
    ".yml",
    ".yaml",
}

SPECIAL_FILES = {
    "Dockerfile",
}


def load_documents():
    documents = []

    # -------------------------------------------------
    # 1. Load university knowledge-base documents
    # -------------------------------------------------
    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text,
            "source_type": "university"
        })

    # -------------------------------------------------
    # 2. Load repository/code/DevOps files
    # -------------------------------------------------
    for file_path in PROJECT_ROOT.rglob("*"):

        if not file_path.is_file():
            continue

        # Skip excluded directories
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue

        # Skip vector-store files explicitly
        try:
            relative_path = file_path.relative_to(PROJECT_ROOT)
        except ValueError:
            continue

        if str(relative_path).startswith("data\\vector_store"):
            continue

        # Only index supported file types
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            if file_path.name not in SPECIAL_FILES:
                continue

        # Avoid indexing the generated vector-store metadata
        if file_path.parent == DATA_DIR / "vector_store":
            continue

        try:
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        if not text.strip():
            continue

        documents.append({
            "filename": str(relative_path),
            "text": text,
            "source_type": "repository"
        })

    return documents