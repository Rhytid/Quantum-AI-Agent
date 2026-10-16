---
name: first-time-setup
description: Finish setting up this workspace on a new computer — install the Python packages, run the setup check, test the PDF step, and explain the result in plain, non-technical language. Use when the user runs /first-time-setup or says they just downloaded/cloned the project, or asks to set it up.
---

Set up this workspace for a user who may be **unfamiliar with computers**. Talk to them in plain
language: no jargon, short sentences, and say what you are doing and why before each step that
needs their permission ("I'm going to install the math libraries the project needs. Please click
Allow."). Never ask them to type commands; run everything yourself.

1. **Find Python.** Try `python --version`, then `python3 --version`, then on Windows
   `py --version`. Use whichever works for every later step.
   - None works: explain that Python isn't installed or wasn't added to PATH. Point them to
     README.md Step 1b, stressing the "Add python.exe to PATH" checkbox (Windows: re-run the
     installer → Modify) and restarting the computer afterwards. Then stop.
   - Version below 3.10: ask them to install the current version from python.org, then stop.
2. **Install packages:** `<python> -m pip install -r tools/requirements.txt`. If pip reports a
   permissions error, retry with `--user`. If it fails another way, show the key error line and
   explain it simply.
3. **Run the check:** `<python> tools/check_setup.py`. Then, if it reports pdflatex was found, run
   `<python> tools/check_setup.py --latex`. Before running it, warn Windows users that "Package
   Installation" windows may pop up (possibly hidden on the taskbar) and they should click
   **Install** in each one. This step can take several minutes the first time.
4. **Report** in plain words as a short checklist (✅ ready / ⚠️ optional thing missing / ❌ needs
   fixing), translating each line of the check:
   - pdflatex missing → "PDFs can't be made yet. Everything else works. To get PDFs, install
     LaTeX (README Step 1d), restart, and run /first-time-setup again."
   - Lean not installed → don't mention it, unless they ask; it's optional and advanced.
   - git not found → only matters if they want you to sync for them; GitHub Desktop works without it.
   For any ❌, give the one concrete fix from README.md's "Getting help" table.
5. If everything required passed, congratulate them and suggest the test from README Step 5:
   `/quantum The Bell state (|00⟩+|11⟩)/√2 has reduced density matrix I/2 on each qubit.`
   Also mention in one line how to stay in sync (GitHub Desktop: Fetch/Pull before working,
   Commit + Push after; or ask you to "pull" / "commit and push").

Do not change any project files during setup.
