"""Bundle this workspace into a zip to send to another computer.

Usage:
    python tools/make_package.py               # everything, including the reference PDFs
    python tools/make_package.py --no-papers   # leave out PDFs and extracted paper text

Writes dist/ClaudeMath-<date>.zip. Leaves out caches, virtual envs, LaTeX build files,
Lean build output, and earlier packages. Unpack it anywhere and follow SETUP.md.
"""
from __future__ import annotations

import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "dist", "__pycache__", ".venv", ".lake", "build", ".ipynb_checkpoints"}
SKIP_SUFFIXES = {".aux", ".log", ".out", ".synctex.gz", ".pyc", ".toc", ".fls", ".fdb_latexmk"}


def wanted(rel: Path, no_papers: bool) -> bool:
    if any(part in SKIP_DIRS for part in rel.parts[:-1]):
        return False
    if any(rel.name.endswith(s) for s in SKIP_SUFFIXES):
        return False
    if no_papers:
        if rel.parts[0] == "Quantum":
            return False
        if rel.parts[0] == "papers" and (rel.suffix.lower() == ".pdf" or rel.parts[1:2] == ("text",)):
            return False
    return True


def main() -> int:
    no_papers = "--no-papers" in sys.argv
    out_dir = ROOT / "dist"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"ClaudeMath-{date.today().isoformat()}{'-nopapers' if no_papers else ''}.zip"

    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and wanted(p.relative_to(ROOT), no_papers))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, Path("ClaudeMath") / p.relative_to(ROOT))

    size = out.stat().st_size / 1e6
    print(f"{len(files)} files -> {out.relative_to(ROOT)} ({size:.1f} MB)")
    if no_papers:
        print("Papers left out: the recipient adds PDFs to Quantum/ and runs /ingest-papers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
