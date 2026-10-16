---
name: compute
description: Verify an algebraic identity, inequality, series, matrix or number-theoretic claim with SymPy/Python, or search for small counterexamples.
argument-hint: <claim to check>
---

Check computationally: $ARGUMENTS

1. Write a script in `scratch/<short-name>.py` using SymPy (exact/symbolic first) and
   mpmath or plain Python for numerics and brute-force search.
2. Prefer exact proof-like checks: `simplify(lhs - rhs) == 0`, `factor`, `solve`, exact
   rational arithmetic. Be aware `simplify` returning nonzero doesn't prove the identity false;
   test numerically at random points to decide.
3. For "for all n" claims, check a range of small cases and look hard for counterexamples
   (edge cases: 0, 1, negatives, primes vs composites, singular matrices).
4. Run it with `python scratch/<short-name>.py` and show the code and output.
5. Conclude with exactly one of:
   - **[Computed] Proved symbolically** — SymPy verified it exactly.
   - **[Computed] Supported** — holds in all tested cases (state which); not a proof.
   - **[Computed] False** — give the counterexample.
   - **Inconclusive** — say why.
