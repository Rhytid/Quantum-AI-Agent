# ClaudeMath — math research workspace

I'm doing advanced math. Always:
- Cite the specific paper and theorem/page for any claim from my papers.
- State clearly when something is your own reasoning vs. from a paper.
- Show proofs step by step and flag any step you're unsure about.

## Layout
- `papers/` and `Quantum/` (subfolders OK) — my reference PDFs. `papers/text/<name>.txt` is extracted text with
  `=== page N ===` markers; `papers/INDEX.md` lists every definition/theorem/lemma by paper and page.
  Run `/ingest-papers` after adding PDFs.
- `notes/` — saved proofs, computations, and results. One Markdown file per topic.
- `scratch/` — throwaway SymPy scripts. `lean/` — Lean 4 + Mathlib project (see `lean/README.md`).
- `tools/` — helper scripts (`pdf_extract.py`; `qmath.py` quantum helpers; `latex_check.py`;
  `latex/qmacros.sty` + `latex/template.tex` for write-ups). `notes/latex/` — LaTeX output.

## Portability (this folder is shared between computers)
- Never write absolute paths (`C:\Users\...`, `/Users/...`) into scripts, notes or LaTeX. Scripts locate
  `tools/` relative to their own file: `sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))`.
- Commands here say `python`; on macOS/Linux use `python3` if `python` isn't found.
- Setup on a new computer: see `README.md` (beginner guide), or run `/first-time-setup`.

## Citation format
`[<paper-key>, Thm 3.2, p. 14]`. Paper keys are the PDF file names without extension.
- Page numbers are **PDF page numbers** (what `=== page N ===` says) unless the paper's own
  printed number is known; say which.
- Never cite from memory. Before citing, find the statement in `papers/text/` and check it
  matches. If you can't find it, say "not found in the papers" — do not guess a theorem number.
- For results not in my papers (standard textbook facts), say "standard result, not from your
  papers" and name a usual source if you know one.

## Labels — tag every non-trivial claim
- **[Paper]** — stated in one of my papers (with citation).
- **[Own reasoning]** — derived here; not in the papers.
- **[Computed]** — checked by running SymPy/Python (say what was run).
- **[Lean-verified]** — compiled in Lean with no `sorry`.
- **[Unsure]** — a step I'm not confident in; say why and what would settle it.

## Proof style
- Number the steps. Each step says what it uses (hypothesis, earlier step, cited result).
- State all hypotheses up front; flag any hypothesis a cited theorem needs that we haven't checked.
- Prefer checking concrete claims (identities, small cases, counterexamples) with SymPy before
  relying on them.
- Use LaTeX (`$...$`, `$$...$$`) for math.

## Agents and skills
- `/prove <statement>` — step-by-step proof using the papers, then an independent check.
- `/check-proof <file or pasted proof>` — adversarial review by the `proof-checker` agent.
- `/compute <claim>` — verify algebra / search for counterexamples in Python.
- `/formalize <statement>` — attempt a Lean 4 proof via the `lean-formalizer` agent.
- `/ingest-papers` — extract text from new PDFs and update `papers/INDEX.md`.
- `/quantum <statement>` — quantum pipeline: `quantum-prover` → `quantum-computer` →
  `proof-checker` → `latex-translator`.
- `/first-time-setup` — finish setup on a new computer (packages + checks), explained in plain language.
- `/to-latex <note>` — translate a note to LaTeX via `latex-translator` (math unchanged).
- `paper-reader` agent — finds and quotes exact statements from the papers.
