# Repository Guidelines

## Project Structure & Module Organization
- `chapters/`: Source for the textbook. Each chapter resides under `partN/chapterNN/` with numbered sections like `4-3.md` and a chapter index `chapterNN.md`.
- `assets/diagrams/`: Figures (prefer SVG). Organize by chapter, e.g., `assets/diagrams/chapter01/`.
- `templates/` and `style-guide.md`: Writing templates and the editorial style. Follow these for structure, tone, and markup.
- `sample-code/questforge/`: Python example project (domain, application, infrastructure, CLI, Streamlit). See `requirements.txt`.
- `.ai/`: Internal agent workflows, commands, and context; do not edit `.ai/tmp/` artifacts.

## Build, Test, and Development Commands
- No global build is required for the book; edit Markdown directly.
- Python sample code (from repo root):
  - Create venv and install deps:
    - Windows: `python -m venv .venv && .venv\\Scripts\\activate && pip install -r sample-code/questforge/requirements.txt`
    - Unix: `python -m venv .venv && source .venv/bin/activate && pip install -r sample-code/questforge/requirements.txt`
  - Run demo: `python sample-code/run_questforge_demo.py`
  - Run GUI: `streamlit run sample-code/questforge/presentation/streamlit_app.py`

## Coding Style & Naming Conventions
- Markdown: Use `templates/` and adhere to `style-guide.md` (headings, tone, code blocks, figure notation). Keep filenames numeric: `partN/chapterNN/N-M.md`.
- Python: PEP 8, 4‑space indents, type hints where practical, module names snake_case, classes PascalCase, functions snake_case. Keep modules small and cohesive.

## Testing Guidelines
- The repo has no centralized test runner. For `sample-code/questforge/`, add `pytest` tests under `sample-code/questforge/tests/` with files named `test_*.py`. Run with `pytest -q` in the venv.
- Prefer fast, focused unit tests around domain and use_case layers.

## Commit & Pull Request Guidelines
- Commits: Prefer Conventional Commits (e.g., `docs:`, `feat:`, `fix:`, `refactor:`) with an imperative, concise subject and a short body when helpful.
- PRs: Include a clear description, linked issues, affected paths (e.g., `chapters/part2/chapter04/`), before/after screenshots for diagrams, and validation notes (commands run, tests added).

## Security & Assets
- Do not commit secrets or large binaries. Use SVG for diagrams. Place example data under `sample-code/questforge/data/` and keep it lightweight.
