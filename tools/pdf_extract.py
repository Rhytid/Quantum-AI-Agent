"""Extract text from PDFs in papers/ and Quantum/ (recursively) into papers/text/<key>.txt.

The paper key is the file name without extension and without a trailing " copy".
Byte-identical duplicates are extracted once; two different files with the same key are
reported and the second is skipped (rename one to fix).

Usage:
    python tools/pdf_extract.py            # extract every PDF that has no .txt yet
    python tools/pdf_extract.py --force    # re-extract everything
    python tools/pdf_extract.py file.pdf   # extract specific files
"""

import argparse
import hashlib
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "papers"
TEXT = PAPERS / "text"
SOURCES = [PAPERS, ROOT / "Quantum"]


def paper_key(pdf: Path) -> str:
    stem = pdf.stem
    return stem[: -len(" copy")] if stem.endswith(" copy") else stem


def extract(pdf: Path, force: bool) -> str:
    out = TEXT / f"{paper_key(pdf)}.txt"
    if out.exists() and not force:
        return f"skip  {pdf.name} (already extracted)"
    reader = PdfReader(pdf)
    parts = []
    empty = 0
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text.strip():
            empty += 1
        parts.append(f"=== page {i} ===\n{text.strip()}\n")
    out.write_text("\n".join(parts), encoding="utf-8")
    note = f"  WARNING: {empty} page(s) had no text (scanned? needs OCR)" if empty else ""
    return f"ok    {pdf.name} -> text/{out.name} ({len(reader.pages)} pages){note}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    TEXT.mkdir(parents=True, exist_ok=True)
    pdfs = [f if f.is_absolute() else Path.cwd() / f for f in args.files] or sorted(
        p for src in SOURCES if src.exists() for p in src.rglob("*.pdf") if TEXT not in p.parents
    )
    if not pdfs:
        print("No PDFs found in papers/ or Quantum/.")
        return 0
    seen: dict[str, tuple[str, Path]] = {}  # key -> (sha256, first path)
    for pdf in pdfs:
        key, digest = paper_key(pdf), hashlib.sha256(pdf.read_bytes()).hexdigest()
        if key in seen:
            if seen[key][0] == digest:
                print(f"dup   {pdf.relative_to(ROOT)} (identical to {seen[key][1].relative_to(ROOT)})")
            else:
                print(f"CLASH {pdf.relative_to(ROOT)}: key '{key}' already used by "
                      f"{seen[key][1].relative_to(ROOT)} with different content; rename one", file=sys.stderr)
            continue
        seen[key] = (digest, pdf)
        try:
            print(extract(pdf, args.force))
        except Exception as e:  # keep going on a bad file
            print(f"FAIL  {pdf.name}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
