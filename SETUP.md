# ClaudeMath: setup on a new computer

A Claude Code workspace for quantum-mathematics research. Give it a statement and it writes a
step-by-step proof citing the reference papers, checks the proof's claims with Python, has an
independent referee review it, and produces a compiled LaTeX PDF.

Everything that drives this (the agents, the `/quantum` command, the citation rules) lives in this
folder (`.claude/` and `CLAUDE.md`), so it works on any computer once the folder is opened in
Claude Code. Nothing needs to be installed into Claude itself.

## 1. Install (one time)

| What | Why | How |
|---|---|---|
| **Claude Code** | Runs the agents | The Claude desktop app (Code tab) or the `claude` CLI, signed in to the Claude account |
| **Python 3.10+** | Computation and paper extraction | Windows: python.org installer, tick "Add python.exe to PATH". macOS: `brew install python` |
| **Python packages** | SymPy, NumPy, SciPy, pypdf | From inside this folder: `python -m pip install -r tools/requirements.txt` |
| **LaTeX** (optional but recommended) | Compiles write-ups to PDF | Windows: MiKTeX. macOS: MacTeX. Linux: TeX Live. Without it, write-ups are still produced and error-checked, just not compiled. |
| **Lean 4** (optional) | Only for `/formalize` | See `lean/README.md`. Skip if you don't need machine-checked proofs. |

On macOS/Linux, use `python3` wherever these instructions say `python`.

**MiKTeX:** the first compile downloads several LaTeX packages. MiKTeX shows a "Package
Installation" window for each one; click **Install**. To stop it asking, uncheck "Always show
this dialog". If the window seems to hang, look for it behind other windows.

You also need **Git** (Windows: git-scm.com, default options; macOS: `xcode-select --install`)
and a GitHub account that has been invited to the repository.

## 2. Get the folder and check it

1. Download (clone) the repository. In a terminal, in the folder where you want it (e.g. `Documents`):
   ```
   git clone https://github.com/Rhytid/Quantum-AI-Agent.git ClaudeMath
   cd ClaudeMath
   python -m pip install -r tools/requirements.txt
   ```
   The first time, a browser window asks you to sign in to GitHub. Paths inside are all
   relative, so the location doesn't matter.
2. In that folder:
   ```
   python tools/check_setup.py
   ```
   Every line should say `ok`, except optional items, which may say `warn`. Add `--latex` to also
   test-compile a document.
3. Open the folder in Claude Code. In the desktop app, pick it as the session's folder; in a
   terminal, run `claude` from inside it. Type `/` and you should see `/quantum`, `/prove`,
   `/compute`, `/check-proof`, `/to-latex`, `/ingest-papers`, `/formalize`.

## 3. Use

| Command | What it does |
|---|---|
| `/quantum <statement>` | Full pipeline: proof → computational checks → referee → LaTeX PDF. Add `--no-check` or `--no-latex` to skip stages. |
| `/prove <statement>` | Proof plus referee, for non-quantum math |
| `/compute <claim>` | Check an identity or look for counterexamples in Python |
| `/check-proof <file or text>` | Skeptical referee review of an existing proof |
| `/to-latex notes/<file>.md` | Turn a note into a LaTeX document and PDF (math unchanged) |
| `/ingest-papers` | After adding PDFs: extract their text and index their theorems |
| `/formalize <statement>` | Lean 4 proof attempt (needs Lean) |

Results are saved as follows:
- `notes/<topic>.md`: the proof and its checks.
- `notes/latex/<topic>.tex` and `.pdf`: the write-up.
- `scratch/`: the Python check scripts.

`notes/depolarizing-cp.md` (and its PDF) is a finished example.

Every claim in a proof is labelled: **[Paper]** (with a citation like
`[<paper-key>, Thm 3.2, p. 14]`, with PDF page numbers unless stated otherwise), **[Own reasoning]**, **[Computed]**, **[Lean-verified]**
or **[Unsure]**. Computational checks say whether they were *proved symbolically* (exact, for
the stated case) or only *supported* (random tests: evidence, not proof). `CLAUDE.md` has the full rules.

## Papers

Reference PDFs go anywhere under `Quantum/` (subfolders are fine) or `papers/`. After adding
any, run `/ingest-papers`. A paper's citation key is its file name without `.pdf`, so give
files stable, descriptive names.

## Staying in sync

The folder is a Git repository shared on GitHub. In a terminal in the folder:

| When | Command |
|---|---|
| Before starting work (get the other person's changes) | `git pull` |
| After finishing something (share your changes) | `git add -A`, then `git commit -m "what you did"`, then `git push` |

You can also just ask Claude Code: "pull the latest changes" or "commit and push my changes".
If you both edited the same file, `git pull` may report a conflict; ask Claude to resolve it.

Check scripts in `scratch/` are local only, not shared (see `.gitignore`).

To send a copy to someone without GitHub access, `python tools/make_package.py` builds a zip in
`dist/` (`--no-papers` leaves out the PDFs).
