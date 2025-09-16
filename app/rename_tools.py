from __future__ import annotations
from pathlib import Path
from typing import List, Optional, Tuple

def batch_rename(
    files: List[Path],
    prefix: str = "",
    suffix: str = "",
    replace_from: Optional[str] = None,
    replace_to: Optional[str] = None,
    start_number: int = 1,
    pad: int = 3,
) -> List[Tuple[Path, Path]]:
    results: List[Tuple[Path, Path]] = []
    seq = start_number
    for f in files:
        stem = f.stem
        if replace_from:
            stem = stem.replace(replace_from, replace_to or "")
        new_name = f"{prefix}{stem}{suffix}_{str(seq).zfill(pad)}{f.suffix}"
        new_path = f.with_name(new_name)
        f.rename(new_path)
        results.append((f, new_path))
        seq += 1
    return results
