from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import List

def read_table(path: Path) -> pd.DataFrame:
    p = Path(path)
    if p.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(p)
    if p.suffix.lower() in {".csv"}:
        return pd.read_csv(p)
    raise ValueError(f"Unsupported file type: {p.suffix}")

def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^0-9A-Za-z_]", "", regex=True)
        .str.lower()
    )
    return df

def merge_and_clean(paths: List[Path], drop_duplicates: bool = True) -> pd.DataFrame:
    frames = []
    for p in paths:
        df = read_table(Path(p))
        df = normalize_headers(df)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    merged = pd.concat(frames, ignore_index=True)
    if drop_duplicates:
        merged = merged.drop_duplicates()
    return merged
