---
name: ingest-papers
description: Extract text from new PDFs in papers/ or Quantum/ and add their definitions, theorems and lemmas (with pages) to papers/INDEX.md. Run after adding reference papers.
---

1. Run `python tools/pdf_extract.py` (add `--force` only if the user asks to redo all).
   If a page had no text, warn the user that the PDF is probably scanned and needs OCR.
2. For each paper whose key isn't yet a section in `papers/INDEX.md`, read
   `papers/text/<paper-key>.txt` and add a section following the template in INDEX.md:
   title, authors, year, one-line topic, and a table of every numbered Definition, Theorem,
   Proposition, Lemma, Corollary, and key unnumbered result, with PDF page and a one-line
   summary including main hypotheses. Note standing assumptions ("throughout, ...") as rows too.
3. Large papers: use one agent per paper in parallel, each returning only its table.
4. Remove the "_No papers yet_" line once there is at least one paper.
5. Report: papers added, number of indexed results each, and any extraction problems
   (garbled math, missing pages).
