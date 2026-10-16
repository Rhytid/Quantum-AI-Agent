---
name: quantum
description: Full pipeline for a quantum-mathematics statement — prove it (quantum-prover), verify its concrete claims computationally (quantum-computer), referee it (proof-checker), and translate the result to LaTeX (latex-translator). Use when the user asks to prove, check, or write up a result about Hilbert-space operators, quantum states, channels, entanglement or quantum information.
argument-hint: <statement> [--no-latex] [--no-check]
---

Run the quantum pipeline on: $ARGUMENTS

Pick a short kebab-case `<topic>` for file names.

1. **Setting.** Restate the statement precisely: dimension (finite or infinite), conventions,
   and what each object is (state, channel, observable). If the statement is ambiguous in a way
   that changes the truth value (e.g. squared vs non-squared fidelity, bounded vs unbounded
   operators), ask the user before continuing. Otherwise state the reading you chose.

2. **Proof generation.** Launch the `quantum-prover` agent with the restated statement and
   output path `notes/<topic>.md`. If it reports a counterexample, skip to step 6.

3. **Computation.** Launch the `quantum-computer` agent with the prover's "Claims to compute"
   list, plus the main statement itself as claim C0 for a randomized small-dimension test.
   - Any **False** verdict: send the counterexample back to `quantum-prover` to repair the
     step. Allow up to 2 repair rounds, then stop and report.
   - Append the verdict table to `notes/<topic>.md` under "Computational checks", and
     upgrade the corresponding steps' labels to **[Computed]** only where the verdict is
     *Proved symbolically*. *Supported* stays as supporting evidence, not proof.

4. **Referee** (skip with `--no-check`). Launch `proof-checker` on `notes/<topic>.md`. Fix ❌
   items via `quantum-prover`. Leave ⚠️ items marked **[Unsure]** if they can't be closed.

5. **LaTeX** (skip with `--no-latex`). Launch `latex-translator` on `notes/<topic>.md` with
   output `notes/latex/<topic>.tex`. It must pass `python tools/latex_check.py`.

6. **Report to the user:**
   - The final statement and proof (or the counterexample), with labels.
   - Computation table: claim | method | verdict.
   - Referee verdict and remaining doubts.
   - File links: `notes/<topic>.md`, `notes/latex/<topic>.tex`, and the scripts in `scratch/`.
   - Offer `/formalize` for steps that are still [Unsure] and could be stated in Mathlib's
     finite-dimensional matrix library.

Steps 2–5 run in sequence because each depends on the one before. Within step 3, the
independent claims may be split across parallel `quantum-computer` agents if there are many.
