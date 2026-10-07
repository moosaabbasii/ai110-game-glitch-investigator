# AI Interactions Log

## Agent Workflow (SF8)

**What task did I give the agent?**

I used Codex as a pair-programming assistant for the Game Glitch Investigator project. I set the goal of producing a complete, submission-ready repair, asked it to inspect the starter code, and directed it to include the required game files, tests, documentation, and Git history.

**What did the agent do?**

Codex inspected the starter specification, proposed fixes for state, comparison, hint, validation, and scoring problems, and drafted the implementation in `app.py`, `logic_utils.py`, and `tests/test_game_logic.py`. It also ran pytest and captured the output in `test_results.txt` so I could review the verification evidence.

**What did I have to verify or fix manually?**

I remained responsible for the project decisions and final review. I set the submission scope, selected the repository name and description, reviewed the required documents, and requested revisions when the AI-interaction wording did not represent my role clearly. The agent’s output was treated as a proposal rather than authority: I still need to run the app and make sure the final walkthrough matches the submitted work. This human-in-the-loop review matters because AI-generated code can be internally consistent while still failing the assignment’s intended behavior.

---

## Test Generation (SF7)

| Edge case | Prompt used | AI-suggested test | Did it pass? | My reasoning |
| --- | --- | --- | --- | --- |
| Reversed hints | “Create a pytest case for both directions of a number-guessing hint.” | Guess 60 vs. secret 50 must include “lower”; guess 40 must include “higher.” | Yes | This tests the player-visible behavior rather than only checking a label. |
| Invalid numeric input | “Test blank, decimal, and non-numeric guesses.” | `None`, blanks, `4.5`, `banana`, and `1e2` are rejected. | Yes | The test set enforces the stated whole-number rule. |
| Scoring floor | “Test a late correct guess.” | A win on attempt 50 earns the 10-point minimum. | Yes | This protects the documented score invariant. |

---

## Linting & Style (SF9)

**Prompt used:**

```text
Review the repaired Python files for clarity, duplicated game rules, and error handling that could hide a bug.
```

**Changes applied:**

The game rules were kept in `logic_utils.py`, comparison uses integers only, and expected invalid inputs return user-facing messages while invalid internal configuration raises `ValueError`.
