from __future__ import annotations
from pathlib import Path
from pypdf import PdfWriter, PdfReader
from typing import List

def merge_pdfs(paths: List[Path], out_path: Path) -> Path:
    writer = PdfWriter()
    for p in paths:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return Path(out_path)
