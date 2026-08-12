from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".md"}

def load_document(path: Path):
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS: raise ValueError("Only PDF, TXT, DOCX, and Markdown files are supported.")
    if suffix == ".pdf": return PyPDFLoader(str(path)).load()
    if suffix == ".docx": return Docx2txtLoader(str(path)).load()
    return TextLoader(str(path), encoding="utf-8").load()

