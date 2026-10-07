# AI Interactions Log

## Agent Workflow (SF8)

**What task did I give the agent?**

I asked Codex to inspect the official Game Glitch Investigator starter, repair the unreliable Streamlit number guessing game, move rules into a testable module, and document the verified result.

**What did the agent do?**

It located the starter specification, identified the state, comparison, hint, validation, and scoring problems, and created `app.py`, `logic_utils.py`, and `tests/test_game_logic.py`. It also ran pytest and captured the output in `test_results.txt`.

**What did I have to verify or fix manually?**

The agent’s implementation was treated as a proposal rather than authority. I reviewed the difficulty ranges and scoring rule, checked that invalid submissions do not use attempts, and used the test output to verify the final behavior. This review matters because an AI-generated solution can be internally consistent while still failing the assignment’s intended behavior.

---

## Test Generation (SF7)

| Edge case | Prompt used | AI-suggested test | Did it pass? | My reasoning |
| --- | --- | --- | --- | --- |
| Reversed hints | “Create a pytest case for both directions of a number-guessing hint.” | Guess 60 vs. secret 50 must include “lower”; guess 40 must include “higher.” | Yes | Tests the bug players see rather than only checking a label. |
| Invalid numeric input | “Test blank, decimal, and non-numeric guesses.” | `None`, blanks, `4.5`, `banana`, and `1e2` are rejected. | Yes | Whole-number input is a stated game rule. |
| Scoring floor | “Test a late correct guess.” | A win on attempt 50 earns the 10-point minimum. | Yes | Protects the documented score invariant. |

---

## Linting & Style (SF9)

**Prompt used:**

```text
Review the repaired Python files for clarity, duplicated game rules, and error handling that could hide a bug.
```

**Changes applied:**

The game rules were kept in `logic_utils.py`, comparison uses integers only, and expected invalid inputs return user-facing messages while invalid internal configuration raises `ValueError`.
