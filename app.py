"""Streamlit interface for Game Glitch Investigator."""

from __future__ import annotations

import random
from typing import Any

import streamlit as st

from logic_utils import (
    DIFFICULTY_RANGES,
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    validate_guess,
)


ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}


def new_game_state(difficulty: str) -> dict[str, Any]:
    """Create all state for one game using the selected difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    return {
        "secret": random.randint(low, high),
        "difficulty": difficulty,
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def reset_game(difficulty: str) -> None:
    """Replace every per-game value, retaining no stale state from prior games."""
    st.session_state.update(new_game_state(difficulty))
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1


def initialise_game(difficulty: str) -> None:
    """Initialize a game once, or intentionally reset it after a difficulty change."""
    if "secret" not in st.session_state:
        reset_game(difficulty)
    elif st.session_state.difficulty != difficulty:
        reset_game(difficulty)


def render_history() -> None:
    """Show previous valid guesses in a compact, readable form."""
    if not st.session_state.history:
        return
    st.subheader("Guess history")
    entries = [
        f"#{item['attempt']}: {item['guess']} — {item['outcome']}"
        for item in st.session_state.history
    ]
    st.write("  ".join(entries))


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("A repaired number guessing game with testable rules.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", list(DIFFICULTY_RANGES), index=1)
initialise_game(difficulty)

low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
st.sidebar.caption(f"Range: {low}–{high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

remaining = attempt_limit - st.session_state.attempts
st.subheader("Make a guess")
st.info(f"Guess a whole number from {low} to {high}. Attempts left: {remaining}")

with st.expander("Developer verification details"):
    st.caption("This panel is retained for the assignment's debugging walkthrough.")
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Status:", st.session_state.status)

input_key = f"guess_input_{st.session_state.game_id}"
raw_guess = st.text_input("Enter your guess", key=input_key, disabled=st.session_state.status != "playing")

submit_col, new_game_col, hint_col = st.columns(3)
with submit_col:
    submit = st.button("Submit Guess 🚀", disabled=st.session_state.status != "playing")
with new_game_col:
    start_over = st.button("New Game 🔁")
with hint_col:
    show_hint = st.checkbox("Show hint", value=True)

if start_over:
    reset_game(difficulty)
    st.rerun()

if submit:
    parsed, guess, error = parse_guess(raw_guess)
    if not parsed:
        st.error(error)
    else:
        in_range, error = validate_guess(guess, low, high)
        if not in_range:
            st.error(error)
        else:
            # Only valid, in-range guesses consume an attempt.
            st.session_state.attempts += 1
            outcome, message = check_guess(guess, st.session_state.secret)
            st.session_state.history.append(
                {
                    "attempt": st.session_state.attempts,
                    "guess": guess,
                    "outcome": outcome,
                }
            )
            st.session_state.score = update_score(
                st.session_state.score, outcome, st.session_state.attempts
            )

            if outcome == "Win":
                st.session_state.status = "won"
                st.balloons()
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts. The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
            elif show_hint:
                st.warning(message)

if st.session_state.status == "won":
    st.success("This game is complete. Choose New Game to play again.")
elif st.session_state.status == "lost":
    st.error("This game is complete. Choose New Game to try again.")

st.metric("Score", st.session_state.score)
render_history()

