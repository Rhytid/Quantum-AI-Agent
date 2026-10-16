---
name: to-latex
description: Translate a note in notes/ (or pasted math) into a compilable LaTeX document using the workspace quantum macros, without changing the mathematics.
argument-hint: <notes/file.md or pasted text> [output.tex]
---

Translate to LaTeX: $ARGUMENTS

1. If the input is pasted text, save it first to `notes/<topic>.md`.
2. Launch the `latex-translator` agent with the source and output path (default
   `notes/latex/<same-name>.tex`).
3. Report the output path, the `tools/latex_check.py` result (compiled, or lint only), and any
   problems in the math the translator flagged but did not change.
