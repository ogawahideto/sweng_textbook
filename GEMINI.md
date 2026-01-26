# Gemini Context: Digital Alchemy Textbook & QuestForge

This repository contains the source material for the textbook **"『「楽しい」ソフトウェア工学の教科書 - デジタル・アルケミー』"** (The "Fun" Software Engineering Textbook - Digital Alchemy) and its accompanying sample application, **QuestForge**.

## 1. Project Overview

*   **Goal:** Co-author a textbook that teaches software engineering through the lens of "Digital Alchemy" — blending traditional engineering aesthetics with modern AI-driven development.
*   **Structure:**
    *   `textbook/`: Root directory containing manuscript and management files.
    *   `chapters/`: The actual manuscript content organized by parts and chapters.
    *   `sample-code/questforge/`: A gamified task management application used as the primary teaching example throughout the book.

## 2. Textbook Authoring (Non-Code)

### Workflow
The writing process involves a collaboration between Human and AI.

1.  **Plan:** Check `progress.md` and use `.ai/workflows/plan-next.md` to determine the next section.
2.  **Draft:** AI generates a draft for a section using `.ai/workflows/draft.md`, adhering to `plan.md` and `style-guide.md`.
3.  **Edit:** Human reviews and refines the draft (Technical accuracy, voice, examples).
4.  **Review:** AI reviews the refined draft using `.ai/workflows/review.md` for quality and consistency.

### Key Files
*   `plan.md`: The outline and goals for every chapter and section.
*   `progress.md`: Tracks the status of each section (⬜ Not Started, 🟨 AI Draft, 🟦 Human Editing, 🟩 Review, ✅ Complete).
*   `style-guide.md`: Defines the tone ("witty," "aesthetic," "practical"), terminology, and formatting rules.
*   `templates/`: Markdown templates for chapters and sections.

## 3. QuestForge Application (Code)

**QuestForge** is a Python-based task management app built with Clean Architecture. It serves as the practical example for the textbook's concepts (DDD, TDD, CI/CD, etc.).

### Tech Stack
*   **Language:** Python 3.x
*   **UI:** Streamlit (Web), CLI
*   **Architecture:** Clean Architecture (Domain, Application, Infrastructure, Presentation layers)
*   **Persistence:** JSON (File-based) / In-Memory (for tests)

### Setup & Usage

**Installation:**
```bash
cd sample-code/questforge
pip install -r requirements.txt
```

**Running the Web UI:**
```bash
# From sample-code/questforge
python -m streamlit run presentation/streamlit_app.py
```
*   Access at: `http://localhost:8501`

**Running the CLI Demo:**
```bash
# From sample-code/
python run_questforge_demo.py
```

**Running Tests:**
```bash
# From sample-code/questforge
python -m unittest discover tests
```

### Directory Structure
*   `domain/`: Entities (Hero, Quest), Value Objects, Repository Interfaces. **No external dependencies.**
*   `application/`: Use Cases (CreateQuest, CompleteQuest). Contains business rules.
*   `infrastructure/`: Implementations of repositories (JSON, Memory), External APIs.
*   `presentation/`: CLI commands and Streamlit app.
*   `cli/`: Command-line interface logic.

## 4. Development & Writing Conventions

*   **Language:** The textbook is written in **Japanese**.
*   **Code Style:** Python code should follow PEP 8.
*   **Tone:** The textbook should be engaging, using metaphors of magic and adventure ("Alchemy," "Grimoires," "Quests") to explain technical concepts.
*   **AI Role:** AI acts as a "Co-author" or "Familiar," assisting with drafting, reviewing, and code generation, but the Human retains the "Architect" role.

## 5. Quick Commands

*   **Check Progress:** `cat progress.md`
*   **Read Style Guide:** `cat style-guide.md`
*   **List Chapters:** `ls -R chapters/`

## Gemini Added Memories
- **Commit Frequency:** Commit changes frequently, ideally after completing each logical unit of work (e.g., finishing a single section draft, completing a refactor, or updating a config file). Do not wait for large batches of changes.
