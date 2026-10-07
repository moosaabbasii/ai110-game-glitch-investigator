"""Pure, testable rules for the Game Glitch Investigator guessing game."""

from __future__ import annotations

from typing import Final


DIFFICULTY_RANGES: Final[dict[str, tuple[int, int]]] = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 200),
}


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive number range for a supported difficulty.

    Raising ``ValueError`` instead of silently using a fallback makes a bad UI
    value visible during development and prevents a game from using the wrong
    range.
    """
    try:
        return DIFFICULTY_RANGES[difficulty]
    except KeyError as error:
        supported = ", ".join(DIFFICULTY_RANGES)
        raise ValueError(
            f"Unknown difficulty {difficulty!r}. Choose one of: {supported}."
        ) from error


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """Convert a text-field value to an integer guess.

    Empty input and non-integers return a clear error rather than throwing an
    exception in the Streamlit app. Decimal values are intentionally rejected:
    the game asks for whole numbers.
    """
    if raw is None or not raw.strip():
        return False, None, "Enter a whole-number guess."

    text = raw.strip()
    try:
        value = int(text)
    except ValueError:
        return False, None, "Enter a whole number, such as 42."

    return True, value, None


def validate_guess(guess: int, low: int, high: int) -> tuple[bool, str | None]:
    """Check whether ``guess`` belongs to the current inclusive game range."""
    if low > high:
        raise ValueError("The lower bound cannot be greater than the upper bound.")
    if not low <= guess <= high:
        return False, f"Choose a number from {low} to {high}."
    return True, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare an integer guess with the secret and return outcome plus hint."""
    if guess == secret:
        return "Win", "🎉 Correct! You found the secret number."
    if guess > secret:
        return "Too High", "📉 Too high — try a lower number."
    return "Too Low", "📈 Too low — try a higher number."


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Return the score after an outcome.

    A correct first guess earns 100 points. Each earlier incorrect valid guess
    reduces that award by 10 points, with a minimum win score of 10. Incorrect
    guesses do not cause alternating or negative score changes.
    """
    if attempt_number < 1:
        raise ValueError("attempt_number must be at least 1.")
    if outcome == "Win":
        return current_score + max(10, 110 - 10 * attempt_number)
    if outcome in {"Too High", "Too Low"}:
        return current_score
    raise ValueError(f"Unknown outcome: {outcome!r}.")
