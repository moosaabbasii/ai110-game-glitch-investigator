# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when I started?

The starter game looked like a normal number guesser, but its behavior did not match what the screen promised. The hint branch called a too-high guess “Go HIGHER” and a too-low guess “Go LOWER,” so following the hint moved the player away from the answer. On alternating attempts, the app converted the secret from an integer to a string, which made comparisons unreliable. It also increased the attempt counter before checking whether input was blank, non-numeric, or outside the current difficulty range.

### Bug reproduction log

| Input / action | Expected behavior | Actual starter behavior | Console output / error |
| --- | --- | --- | --- |
| Secret `50`, guess `60` | Outcome: `Too High`; hint tells player to go lower. | The outcome said `Too High`, but the hint said “Go HIGHER!” | No exception; incorrect player guidance. |
| Secret `50`, guess `40` | Outcome: `Too Low`; hint tells player to go higher. | The outcome said `Too Low`, but the hint said “Go LOWER!” | No exception; incorrect player guidance. |
| Submit `hello` | Display an error without using an attempt. | `attempts` increased before parsing rejected the input. | “That is not a number.” after an attempt was consumed. |
| Submit an integer on an alternating attempt | Compare two integers and give a deterministic result. | The code changed `secret` to `str(secret)` on even attempts. | Type-dependent behavior hidden by a broad exception handler. |
| Start a new Hard game | Reset all game fields and choose a number in the Hard range. | The secret was regenerated from 1–100 and score/history/status were not reset. | No exception; stale state carried forward. |

## 2. How did I use AI as a teammate?

I used Codex as an AI pair programmer to inspect the supplied starter implementation, identify its state and logic defects, and propose a small refactor. One useful suggestion was to move parsing, comparison, validation, and scoring into a module with no Streamlit dependency; I verified that choice by testing those functions directly with pytest. I did not accept a broad `try/except TypeError` as a permanent comparison strategy because it hides the real type bug instead of preventing it. I changed the design so inputs are parsed once and the secret stays an integer, then checked the behavior with success and failure cases.

## 3. Debugging and testing my fixes

I treated a fix as complete only when its rule was explicit in code and a test exercised the relevant input or boundary. The pytest suite checks all three difficulty ranges, valid and invalid parsing, inclusive range endpoints, both hint directions, scoring on early and late wins, and invalid function arguments. For example, `test_check_guess_returns_correct_outcome_and_direction` verifies that a guess of 60 against a secret of 50 returns `Too High` and a message containing “lower.” AI helped generate a first pass at edge cases, but I reviewed the expected outcomes and added tests for the specific defects observed in the starter code.

## 4. What did I learn about Streamlit and state?

Streamlit reruns the script from top to bottom after an interaction, so an ordinary variable is recreated on every button click. `st.session_state` is the place to keep values that belong to the player’s current game, such as the secret number, attempts, score, status, and history. The fix is not merely storing one value: related values must be initialized together and reset together, especially when the player starts a new game or changes difficulty. This is a human-in-the-loop decision because a suggested state change must be checked against the game’s actual lifecycle.

## 5. Looking ahead: my developer habits

I want to keep the habit of turning each reported bug into a small reproduction case before changing implementation code. Next time I work with an AI assistant, I will ask it to state assumptions and suggest focused tests before I accept a patch. This project showed me that an AI can hallucinate a plausible implementation that still has incorrect branches, hidden type conversions, or incomplete state resets. A small test set and explicit verification make it much easier to evaluate generated code critically.
