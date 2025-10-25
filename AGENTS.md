# Repository Guidelines
This guide captures the expectations for maintaining and extending the NumPy + Pygame Tetris implementation. Follow it to keep gameplay responsive, code predictable, and changes easy for collaborators to review.

## Project Structure & Module Organization
- `tetris.py` contains the full game loop, state management, and rendering helpers; keep gameplay logic in this module unless you are actively refactoring into packages.
- `requirements.txt` locks the runtime dependencies (`numpy`, `pygame`). Update it whenever you add or bump libraries.
- `README.md` is the player-facing quick start. Mirror any installation or control changes there. Add new assets under a dedicated folder (e.g., `assets/`) and document usage.

## Build, Test, and Development Commands
- `python -m pip install -r requirements.txt` — install or update dependencies in the current environment.
- `python tetris.py` — launch the local game window for manual testing.
- `python -m pip install pygame --pre` — fallback install path for Windows users encountering binary issues (matches README guidance).
Run commands from the repository root; on Windows PowerShell, prefix with `python` as shown above.

## Coding Style & Naming Conventions
- Target Python 3.8+ and follow PEP 8 defaults: 4-space indentation, snake_case for functions and variables, UPPER_CASE for constants (`TETROMINOS`, `SOFT_DROP_FACTOR`).
- Keep game state dictionaries consistently keyed as in `new_piece` (`shape`, `r`, `c`, `color`).
- Prefer small, single-purpose helpers; add concise docstrings when behavior is non-obvious.

## Testing Guidelines
- There is no automated suite yet; smoke-test every change by running `python tetris.py` and exercising rotations, soft drops, and level-ups.
- If you introduce logic that can be unit-tested, add a `tests/` package and use `pytest` or the standard library `unittest`. Name files `test_<feature>.py` and include reproducible board-state scenarios.

## Commit & Pull Request Guidelines
- Use imperative, present-tense commit subjects under 60 characters (e.g., `Add soft-drop gravity factor`).
- Keep commits scoped: gameplay mechanics, rendering tweaks, and dependency updates should land separately.
- Pull requests should describe gameplay impact, note any key bindings or speed changes, and include screenshots or GIFs if visuals are affected.
- Link issues when available and confirm local playtesting steps in the PR description.

## Platform & Configuration Tips
- Running Pygame requires an active display; on headless setups export `SDL_VIDEODRIVER=dummy` for logic-only verification.
- When sharing builds, bundle font or sprite assets alongside `tetris.py` to avoid runtime file errors.
