---
name: check-proof
description: Referee an existing proof (pasted, or in a file) step by step, verify its citations against the papers, and test concrete claims with SymPy.
argument-hint: <file path or pasted proof>
---

Check this proof: $ARGUMENTS

If it's a file path, read it. Pass the full proof to the `proof-checker` agent. Then present its
verdict, the step table, and the list of problems. Keep the checker's findings separate from
any comments of your own, and label those [Own reasoning]. Don't change the user's proof
unless they ask.
