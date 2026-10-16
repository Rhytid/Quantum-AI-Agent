# Quantum AI Agent

An AI research assistant for quantum mathematics. You type a math statement in plain words, and it:

1. **writes a step-by-step proof**, citing the research papers included here,
2. **checks the proof's calculations** with the computer,
3. **has a second AI review the proof** for mistakes, and
4. **produces a polished PDF** of the result.

It runs inside the **Claude** app. This guide walks you through setting it up, one step at a
time. You don't need any technical experience, and you won't need to type any commands.
**Plan on about 30–45 minutes**, most of it waiting for downloads.

> **If you get stuck at any point**, skip to [Getting help](#getting-help) at the bottom.

---

## Before you start

You need:

- **A computer running Windows or macOS** (a Mac). Steps that differ between the two are marked 🪟 **Windows** and 🍎 **Mac**.
- **The Claude account** this project is shared under, with its email and password.
- **A GitHub account that has been invited to this project.** GitHub is the website where the
  project is stored. If you don't have an account, create a free one at
  [github.com/signup](https://github.com/signup), then send your **GitHub username** to the
  person who shared this project so they can invite you. You'll get an email invitation; open it
  and click **Accept invitation**.

---

## Step 1: Install four programs

Install these one at a time. For each: click the link, download the installer, open the
downloaded file (usually in your **Downloads** folder), and follow the instructions below.

### 1a. Claude

[claude.ai/download](https://claude.ai/download). Install it, open it, and sign in to the Claude account.

### 1b. Python (the program that does the math checking)

Go to [python.org/downloads](https://www.python.org/downloads/) and click the big yellow **Download Python** button.

- 🪟 **Windows:** when the installer opens, **tick the box "Add python.exe to PATH"** at the
  bottom of the first screen before clicking **Install Now**. This box is easy to miss, and
  the project won't work without it. If you missed it, run the installer again, choose
  **Modify**, and tick it.
- 🍎 **Mac:** click **Continue** / **Agree** / **Install** through each screen. When it
  finishes, a folder window opens; you can close it.

### 1c. GitHub Desktop (downloads the project and keeps it up to date)

[desktop.github.com](https://desktop.github.com). Install it, open it, and choose **Sign in to
GitHub.com**. Your web browser opens; sign in and click **Authorize**. Back in GitHub Desktop,
click through the remaining screens with the default choices.

### 1d. LaTeX (creates the PDFs). Optional, but recommended

Without this, everything still works except the final PDF step.

- 🪟 **Windows:** [miktex.org/download](https://miktex.org/download). Click **Download**, run the
  installer, and accept the defaults on every screen.
- 🍎 **Mac:** [tug.org/mactex](https://www.tug.org/mactex/) → **MacTeX.pkg**. This is a large
  download (about 5 GB), so start it and go do something else.

**When you're done with all four, restart your computer.** This makes sure the new programs
can find each other.

---

## Step 2: Download the project

1. Open **GitHub Desktop**.
2. In the top menu, click **File** → **Clone repository…** ("clone" just means "download a copy").
3. Click the **GitHub.com** tab and click **Rhytid/Quantum-AI-Agent** in the list.
   (If it's not there, you haven't accepted the invitation email yet; see "Before you start".)
4. The **Local path** box shows where the project will be saved, normally a folder like
   `Documents\GitHub\Quantum-AI-Agent`. **Write this location down.** You'll need it in Step 3.
5. Click **Clone** and wait for it to finish. It's about 60 MB.

---

## Step 3: Open the project in Claude

1. Open the **Claude** app and click **Code** at the top of the window.
2. Start a new session. When it asks which **folder** to work in, choose the
   **Quantum-AI-Agent** folder from Step 2. Pick that exact folder, not the folder that
   contains it.

---

## Step 4: Let Claude finish the setup

In the message box, type this and press Enter:

```
/first-time-setup
```

Claude installs the last pieces and checks that everything works. It may ask for permission
before running things; click **Allow** each time. When it's done, it tells you in plain words
whether everything is ready, and what to do if something isn't.

**🪟 Windows with MiKTeX:** while Claude tests the PDF step, small windows titled
**"Package Installation"** may pop up. Each time, click **Install**. These sometimes hide
behind other windows, so if nothing seems to be happening, check your taskbar. This only
happens the first time.

---

## Step 5: Try it

Type this into Claude and press Enter:

```
/quantum The Bell state (|00⟩+|11⟩)/√2 has reduced density matrix I/2 on each qubit.
```

It takes a few minutes. When it finishes, Claude shows you the proof and tells you where the PDF
was saved, inside the project's `notes/latex` folder.

🎉 **You're set up.**

---

## Everyday use

### Things you can type into Claude

| Type this… | …to do this |
|---|---|
| `/quantum` followed by a statement | The full process: proof, computer checks, review, and PDF |
| `/prove` followed by a statement | A proof for math that isn't about quantum topics |
| `/compute` followed by a formula or claim | Check whether something is true with the computer |
| `/check-proof` followed by a proof (or a file name) | Have a proof reviewed for mistakes |
| `/to-latex notes/` + a file name | Turn a saved proof into a PDF |
| `/ingest-papers` | After adding new papers (see below) |

You can also just ask questions in normal sentences, like "what does the Horodecki paper say
about entanglement witnesses?"

### Reading the results

Every statement in a proof gets a tag telling you where it came from:

- **[Paper]**: from one of the included research papers. The paper and page are named.
- **[Own reasoning]**: worked out by the AI itself.
- **[Computed]**: checked by a computer calculation.
- **[Unsure]**: the AI isn't confident about this step and explains why. **Read these carefully.**

A computer check marked **"Proved symbolically"** is exact. One marked **"Supported"** passed
many random tests, which is good evidence but not a proof.

### Staying in sync with your collaborator

You and your collaborator each have your own copy of the project. GitHub Desktop keeps them
matched:

- **Before you start working, get their latest changes.** Open GitHub Desktop and click
  **Fetch origin** at the top. If it changes to **Pull origin**, click that too.
- **After you finish something, share your changes:**
  1. In GitHub Desktop, the left side lists the files you changed.
  2. At the bottom left, type a short description in the **Summary** box, such as "Added proof about entanglement".
  3. Click **Commit to main**.
  4. Click **Push origin** at the top.

Or just tell Claude **"pull the latest changes"** or **"commit and push my changes"**, and it
does this for you.

### Adding new research papers

1. Copy the PDF files into the project's **Quantum** folder. Subfolders are fine.
2. In Claude, type `/ingest-papers`.
3. Share them using the steps above, so your collaborator gets them too.

A paper is referred to by its file name, so give files clear names like `smith-entanglement-2024.pdf`.

---

## Getting help

The easiest fix for almost anything: **describe the problem to Claude** in the project's Code
session, for example "the setup check says Python is missing, what do I do?". Claude can see
the project's files and walk you through it.

Common problems:

| Problem | Fix |
|---|---|
| Claude says **Python isn't found** | 🪟 Run the Python installer again, choose **Modify**, tick **"Add python.exe to PATH"**, then restart your computer. |
| The project isn't listed in GitHub Desktop's **Clone** window | Accept the invitation email from GitHub first, then try again. |
| **No PDF** is produced | LaTeX (Step 1d) isn't installed. Everything else still works. |
| Claude seems **frozen** while making a PDF | 🪟 Look for a hidden **Package Installation** window on the taskbar and click **Install**. |
| **`/quantum` doesn't appear** when you type `/` | Claude is open in the wrong folder. Start a new Code session and pick the **Quantum-AI-Agent** folder itself (Step 3). |
| GitHub Desktop says there's a **conflict** | You and your collaborator changed the same file. Ask Claude: "help me resolve the merge conflict". |

---

<details>
<summary><b>Technical reference (for experienced users and for Claude)</b></summary>

**Manual setup without GitHub Desktop or `/first-time-setup`:**
```
git clone https://github.com/Rhytid/Quantum-AI-Agent.git
cd Quantum-AI-Agent
python -m pip install -r tools/requirements.txt
python tools/check_setup.py --latex
```
Use `python3` on macOS/Linux. Python 3.10+ is required.

**Optional:** Lean 4 for `/formalize` (machine-checked proofs); see `lean/README.md`.

**Layout and rules:** see `CLAUDE.md`. Scripts in `scratch/` are local only (git-ignored).

**Offline copy:** `python tools/make_package.py` builds a zip in `dist/` (`--no-papers` leaves
out the PDFs).

</details>
