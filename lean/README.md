# Lean 4 + Mathlib setup (one-time, ~5 GB disk)

Lean isn't installed yet. In PowerShell:

1. Install elan (Lean's version manager) — see the official guide:
   https://leanprover-community.github.io/install/windows.html
2. Restart the terminal, then from the `ClaudeMath` folder:

   ```powershell
   lake +leanprover-community/mathlib4:lean-toolchain new lean math
   cd lean
   lake exe cache get
   lake build
   ```

   (If `lake new` refuses because `lean/` exists, move this README out, run it, and move it back.)
3. Create `lean/ClaudeMath/` for formalized results. Check a file with
   `lake env lean ClaudeMath/Foo.lean`.

Optional: install VS Code's "Lean 4" extension to see goals interactively.
