---
name: prove
description: Write a rigorous step-by-step proof of a statement, citing the user's papers, then have it independently checked. Use when the user asks to prove, show, or derive something.
argument-hint: <statement to prove>
---

Prove: $ARGUMENTS

1. **Restate** the claim precisely with all hypotheses and notation. If it's ambiguous or
   looks false, say so and test it on small cases (`/compute`-style SymPy check) before going on.
2. **Gather results.** Use the `paper-reader` agent to find relevant definitions and theorems
   in the papers, with exact statements and pages.
3. **Plan.** One paragraph: proof strategy and the key cited results.
4. **Proof.** Numbered steps. Each step names what it uses and carries a label:
   [Paper] with citation, [Own reasoning], [Computed], or [Unsure] with the reason.
   For every cited theorem, explicitly check each of its hypotheses.
5. **Check.** Send the proof to the `proof-checker` agent. Fix every ❌ and ⚠️ it reports,
   or keep them marked [Unsure] if you can't.
6. **Summary.** Final proof, the checker's verdict, and a short list of remaining doubts.
7. Offer to save it to `notes/<topic>.md` and to try `/formalize`.
