"""Check a .tex file: compile with pdflatex (twice) if available, else run a static lint.

Usage: python tools/latex_check.py notes/latex/<name>.tex   (compiles with pdflatex if on PATH)

The lint catches the common failures without a TeX install: unbalanced braces/brackets,
unmatched \\begin/\\end, unbalanced $ / $$ / \\( \\) / \\[ \\], and macros that are neither
standard nor defined in tools/latex/qmacros.sty or the file itself.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STY = ROOT / "latex" / "qmacros.sty"

# Standard LaTeX / amsmath / amssymb / mathtools / hyperref commands we expect to see.
STANDARD = set("""
documentclass usepackage begin end title author date maketitle section subsection subsubsection
paragraph label ref eqref cite bibitem emph textbf textit texttt textrm textsf mathrm mathbf mathit
mathcal mathbb mathsf mathfrak boldsymbol bm text item frac dfrac tfrac sqrt sum prod int oint lim
limsup liminf sup inf max min log ln exp sin cos tan sinh cosh tanh arcsin arccos arctan det dim ker
deg gcd Pr arg left right middle big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr quad qquad
cdot cdots ldots dots vdots ddots times otimes oplus bigotimes bigoplus circ leq geq le ge neq
approx equiv sim simeq cong propto to mapsto rightarrow leftarrow Rightarrow Leftarrow
Leftrightarrow leftrightarrow iff implies impliedby infty partial nabla forall exists nexists in
notin ni subset subseteq supset supseteq cup cap bigcup bigcap setminus emptyset varnothing
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi
varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi
Pi Sigma Upsilon Phi Psi Omega hat tilde bar vec dot ddot overline underline widehat widetilde
overbrace underbrace langle rangle lvert rvert lVert rVert vert Vert mid dagger ast star pm mp
operatorname DeclareMathOperator newcommand renewcommand providecommand newtheorem theoremstyle
qedhere qed square blacksquare Box today hspace vspace noindent newline linebreak pagebreak
newpage clearpage footnote url href hypersetup tableofcontents appendix label nonumber notag
tag displaystyle textstyle scriptstyle ell hbar Re Im wedge vee neg lnot land lor top bot perp
parallel prime colon coloneqq eqqcolon vdash models binom choose pmod bmod mod not
langle rangle lceil rceil lfloor rfloor uparrow downarrow updownarrow hookrightarrow
twoheadrightarrow xrightarrow overset underset stackrel substack limits nolimits mathop
mathbin mathrel mathord phantom vphantom hphantom smash centering raggedright small
footnotesize scriptsize tiny large Large LARGE huge Huge normalsize caption includegraphics
textsuperscript textsubscript leqslant geqslant ll gg lesssim gtrsim succ prec succeq preceq
trianglelefteq triangleleft triangleright diamond bullet odot ominus boxtimes ltimes rtimes
iint iiint idotsint aleph beth imath jmath wp emph label ensuremath relax par S P dag
hline cline toprule midrule bottomrule cmidrule multicolumn multirow textwidth linewidth columnwidth
arraystretch tabcolsep extracolsep setlength addtolength hfill vfill hfil smallskip medskip bigskip
setcounter addtocounter arabic roman alph cite nocite bibliographystyle bibliography input include
maketitle thanks and lbrack rbrack ss textbackslash textasciitilde dots ldots enspace thinspace
fbox mbox makebox framebox parbox minipage figure table tabularx
thebibliography enumerate itemize description align equation gather multline split cases
pmatrix bmatrix vmatrix Vmatrix matrix smallmatrix array tabular proof theorem lemma
""".split())

TOKEN = re.compile(r"\\([A-Za-z@]+)\*?")


def defined_macros(text: str) -> set[str]:
    pats = [
        r"\\(?:re|provide)?newcommand\*?\s*\{?\\([A-Za-z@]+)",
        r"\\DeclareMathOperator\*?\s*\{\\([A-Za-z@]+)",
        r"\\def\\([A-Za-z@]+)",
        r"\\DeclareUrlCommand\s*\{?\\([A-Za-z@]+)",
        r"\\newif\\if([A-Za-z@]+)",
    ]
    out = set()
    for p in pats:
        out |= set(re.findall(p, text))
    out |= {m for m in re.findall(r"\\newif\\(if[A-Za-z@]+)", text)}
    return out


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def lint(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    text = strip_comments(raw)
    problems: list[str] = []
    lines = text.splitlines()

    # Braces/brackets (ignore escaped \{ \}).
    depth = 0
    for n, line in enumerate(lines, 1):
        for m in re.finditer(r"(?<!\\)[{}]", line):
            depth += 1 if m.group() == "{" else -1
            if depth < 0:
                problems.append(f"line {n}: unmatched '}}'")
                depth = 0
    if depth:
        problems.append(f"{depth} unclosed '{{' in file")

    # Environments.
    stack: list[tuple[str, int]] = []
    for n, line in enumerate(lines, 1):
        for kind, env in re.findall(r"\\(begin|end)\{([^}]+)\}", line):
            if kind == "begin":
                stack.append((env, n))
            elif not stack:
                problems.append(f"line {n}: \\end{{{env}}} without \\begin")
            elif stack[-1][0] != env:
                problems.append(f"line {n}: \\end{{{env}}} closes \\begin{{{stack[-1][0]}}} from line {stack[-1][1]}")
                stack.pop()
            else:
                stack.pop()
    for env, n in stack:
        problems.append(f"line {n}: \\begin{{{env}}} never closed")

    # Math delimiters.
    body = re.sub(r"\\\$", "", text)
    dd = body.count("$$")
    if dd % 2:
        problems.append("odd number of $$")
    if body.replace("$$", "").count("$") % 2:
        problems.append("odd number of $ (unclosed inline math)")
    for o, c in (("\\(", "\\)"), ("\\[", "\\]")):
        if body.count(o) != body.count(c):
            problems.append(f"{o} count {body.count(o)} != {c} count {body.count(c)}")

    # Unknown macros.
    known = STANDARD | defined_macros(text)
    if STY.exists():
        known |= defined_macros(STY.read_text(encoding="utf-8"))
    known |= {"if" + x for x in known} | {"fi", "else"}
    unknown: dict[str, int] = {}
    for n, line in enumerate(lines, 1):
        for name in TOKEN.findall(line):
            if name not in known and name not in unknown:
                unknown[name] = n
    for name, n in unknown.items():
        problems.append(f"line {n}: unknown macro \\{name} (not standard, not in qmacros.sty)")
    return problems


def find_pdflatex() -> str | None:
    """pdflatex on PATH, else the standard MiKTeX / TeX Live install locations.

    The fallback matters on Windows: an app started before TeX was installed keeps the old PATH.
    """
    import os
    found = shutil.which("pdflatex")
    if found:
        return found
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/MiKTeX/miktex/bin/x64/pdflatex.exe",
        Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "MiKTeX/miktex/bin/x64/pdflatex.exe",
    ]
    candidates.append(Path("/Library/TeX/texbin/pdflatex"))  # MacTeX
    candidates += sorted(Path("C:/texlive").glob("*/bin/windows/pdflatex.exe"), reverse=True)
    candidates += sorted(Path("C:/texlive").glob("*/bin/win64/pdflatex.exe"), reverse=True)
    return next((str(c) for c in candidates if c.is_file()), None)


def compile_tex(path: Path, pdflatex: str) -> int:
    # pdflatex run twice (resolves \ref/\cite) rather than latexmk, which needs Perl on MiKTeX.
    import os
    env_dir = str(STY.parent)
    # Trailing separator keeps the default search path (TeX Live and MiKTeX both honor TEXINPUTS).
    env = dict(os.environ, TEXINPUTS=env_dir + os.pathsep + os.environ.get("TEXINPUTS", "") + os.pathsep)
    cmd = [pdflatex, "-interaction=nonstopmode", "-halt-on-error", path.name]
    for _ in range(2):
        r = subprocess.run(cmd, cwd=path.parent, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode:
            break
    if r.returncode:
        errs = [l for l in r.stdout.splitlines() if l.startswith("!") or l.startswith("l.")]
        print("COMPILE FAILED\n" + "\n".join(errs[:30]))
    else:
        print(f"COMPILED OK -> {path.with_suffix('.pdf')}")
    return r.returncode


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1]).resolve()
    problems = lint(path)
    if problems:
        print("LINT PROBLEMS:\n  " + "\n  ".join(problems))
    else:
        print("LINT OK")
    pdflatex = find_pdflatex()
    if pdflatex:
        return compile_tex(path, pdflatex) or (1 if problems else 0)
    print("(no pdflatex found: lint only, not compiled)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
