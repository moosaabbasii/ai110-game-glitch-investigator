# 🎮 Game Glitch Investigator: The Impossible Guesser

This project repairs an AI-generated Streamlit number guessing game. The player selects a difficulty, tries to find a randomly selected secret number within a limited number of valid attempts, and receives accurate direction hints. The repaired version keeps the secret number stable during a game, validates input before spending an attempt, and uses predictable scoring.

## Repairs completed

| Glitch | Cause | Repair |
| --- | --- | --- |
| The game state was inconsistent across Streamlit reruns. | Per-game values were not reset together or tied to the active difficulty. | `st.session_state` now owns one complete game state; it is initialized once and reset deliberately for a new game or a difficulty change. |
| Hints told the player to move in the wrong direction. | The comparison labels and messages were reversed. | `check_guess()` returns `Too High` with a lower-number hint and `Too Low` with a higher-number hint. |
| Some submissions compared an integer to a string. | The original app converted the secret number on alternating attempts. | All valid guesses and the secret remain integers. |
| Invalid and out-of-range entries spent attempts. | The attempt counter increased before input validation. | Parsing and range validation happen before history and attempt state are updated. |
| The score changed unpredictably for misses. | The original formula alternated penalties and bonuses. | Only a win changes the score: 100 points on the first valid attempt, minus 10 per earlier valid miss, with a 10-point minimum. |

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Run the automated tests with:

```powershell
python -m pytest tests/
```

## Demo walkthrough

1. Run the Streamlit command and open the local page shown in the terminal.
2. Select **Easy** to play within the range 1–20 with six valid guesses.
3. Expand **Developer verification details** and note the secret number for the assignment’s debugging demonstration.
4. Submit a number below the secret and confirm the game says to try a higher number; submit one above it and confirm the inverse hint.
5. Submit the secret number and confirm the win message, score, and stored guess history. Choose **New Game** to confirm the attempts, score, history, and secret are reset together.

## Test results

The current verification command and captured output are in [`test_results.txt`](test_results.txt). The suite exercises difficulty ranges, parsing, boundary validation, hint direction, scoring, and invalid inputs.

## Project structure

```text
app.py                    # Streamlit interface and session-state lifecycle
logic_utils.py            # Pure game rules
tests/test_game_logic.py  # pytest verification suite
reflection.md             # Reproduction log and AI collaboration reflection
ai_interactions.md        # Stretch-feature documentation for AI-assisted tests/workflow
```

## Stretch features

The game includes difficulty-specific ranges, an attempt limit, a guess history, input validation, and a transparent scoring rule. `ai_interactions.md` documents the AI-assisted test-generation and agent-workflow stretch work.
