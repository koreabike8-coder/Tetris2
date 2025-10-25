# GitHub Copilot instructions for Tetris

This file provides quick guidance for GitHub Copilot and contributors working on this repository.

- Python: 3.11+
- Run: `python tetris.py` (from the repository root)
- Dependencies: `pip install -r requirements.txt`
- Style: follow PEP 8 (4-space indentation). Keep functions small and readable.
- Tests: use `pytest` if tests are added. There are no automated tests by default.
- Assets: place fonts, sprites or other assets under `assets/` and document usage in README.md.
- Game constants: visual/layout constants live in `tetris.py` (e.g. `CELL_SIZE`, `COLS`, `ROWS`).
- Commit message style: short imperative subject under 60 chars, e.g. `Add soft-drop gravity`.
- When asking Copilot: provide context (file path, goal, and preferred style). If you want a new file created,
  paste the suggested content into a new file in `.github/` and commit it so it is tracked by git.

If you want this file to be copied from another project automatically, run a local `cp` command or use
the workspace Copilot Chat to generate and save the content interactively.
