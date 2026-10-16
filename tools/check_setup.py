"""Check that this computer can run the ClaudeMath workspace.

Usage:
    python tools/check_setup.py           # Python, packages, helper library, LaTeX lint
    python tools/check_setup.py --latex   # also compile a test document (MiKTeX may ask to install packages)
"""
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OK, WARN, FAIL = "  ok  ", " warn ", " FAIL "
failures = 0


def report(status: str, msg: str) -> None:
    global failures
    failures += status == FAIL
    print(f"[{status}] {msg}")


def main() -> int:
    # Python
    v = sys.version_info
    report(OK if v >= (3, 10) else FAIL, f"Python {v.major}.{v.minor}.{v.micro} (need 3.10+)")

    # Packages
    missing = []
    for mod in ("sympy", "mpmath", "numpy", "scipy", "pypdf"):
        try:
            m = importlib.import_module(mod)
            report(OK, f"{mod} {getattr(m, '__version__', '')}")
        except ImportError:
            missing.append(mod)
            report(FAIL, f"{mod} not installed")
    if missing:
        print(f"         fix: python -m pip install -r tools/requirements.txt")

    # Helper library self-test
    if not missing:
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "qmath.py")], capture_output=True, text=True)
        report(OK if r.returncode == 0 else FAIL,
               "qmath.py self-test" + ("" if r.returncode == 0 else f": {r.stderr.strip()[-300:]}"))

    # Papers
    texts = list((ROOT / "papers" / "text").glob("*.txt"))
    pdfs = [p for d in ("papers", "Quantum") if (ROOT / d).exists() for p in (ROOT / d).rglob("*.pdf")]
    report(OK if texts else WARN,
           f"{len(pdfs)} PDFs, {len(texts)} extracted texts"
           + ("" if texts or not pdfs else " (run /ingest-papers in Claude Code)"))

    # LaTeX
    from latex_check import find_pdflatex, lint
    template = ROOT / "tools" / "latex" / "template.tex"
    problems = lint(template)
    report(OK if not problems else FAIL, "LaTeX lint on template" + ("" if not problems else f": {problems}"))
    pdflatex = find_pdflatex()
    if not pdflatex:
        report(WARN, "pdflatex not found: write-ups will be linted but not compiled "
                     "(install MiKTeX on Windows, MacTeX on macOS, TeX Live on Linux)")
    else:
        report(OK, f"pdflatex: {pdflatex}")
        if "--latex" in sys.argv:
            with tempfile.TemporaryDirectory() as tmp:
                doc = Path(tmp) / "setup_test.tex"
                doc.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
                env = dict(os.environ, TEXINPUTS=str(template.parent) + os.pathsep + os.pathsep)
                r = subprocess.run([pdflatex, "-interaction=nonstopmode", "-halt-on-error", doc.name],
                                   cwd=tmp, env=env, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace")
                report(OK if r.returncode == 0 else FAIL, "test compile"
                       + ("" if r.returncode == 0 else ": " + " | ".join(
                           l for l in r.stdout.splitlines() if l.startswith("!"))[:300]))
        else:
            print("         (run with --latex to also test-compile; MiKTeX may ask to install packages)")

    # Optional extras
    report(OK if shutil.which("git") else WARN, "git " + ("found" if shutil.which("git") else
           "not found (optional; used only for the author name in write-ups)"))
    lake = shutil.which("lake")
    print(f"[ info ] Lean: {'found' if lake else 'not installed (optional, only for /formalize; see lean/README.md)'}")

    print("\nAll required checks passed." if not failures else f"\n{failures} required check(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
