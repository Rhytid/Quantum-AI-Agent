---
name: formalize
description: Formalize a statement (and proof, if given) in Lean 4 + Mathlib and check it compiles.
argument-hint: <statement> [informal proof]
---

Formalize in Lean: $ARGUMENTS

Hand this to the `lean-formalizer` agent, including the informal proof if there is one.
When it returns, show the user the Lean statement next to the informal one and point out any
difference in meaning. Only call the result [Lean-verified] if the agent confirms it compiled
with no `sorry` and only standard axioms. If Lean isn't set up, point the user to `lean/README.md`.
