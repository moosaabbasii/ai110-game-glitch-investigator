"""Tests for the pure game rules in logic_utils.py."""

import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
    validate_guess,
)


@pytest.mark.parametrize(
    ("difficulty", "expected_range"),
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 200)),
    ],
)
def test_difficulty_ranges(difficulty, expected_range):
    assert get_range_for_difficulty(difficulty) == expected_range


def test_unknown_difficulty_is_not_silently_accepted():
    with pytest.raises(ValueError, match="Unknown difficulty"):
        get_range_for_difficulty("Expert")


@pytest.mark.parametrize("raw", [None, "", "   ", "4.5", "banana", "1e2"])
def test_parse_guess_rejects_empty_and_non_integer_input(raw):
    ok, value, error = parse_guess(raw)
    assert ok is False
    assert value is None
    assert error


def test_parse_guess_accepts_whole_number_with_spaces():
    assert parse_guess(" 42 ") == (True, 42, None)


@pytest.mark.parametrize(
    ("guess", "secret", "expected_outcome", "hint_fragment"),
    [
        (50, 50, "Win", "Correct"),
        (60, 50, "Too High", "lower"),
        (40, 50, "Too Low", "higher"),
    ],
)
def test_check_guess_returns_correct_outcome_and_direction(
    guess, secret, expected_outcome, hint_fragment
):
    outcome, message = check_guess(guess, secret)
    assert outcome == expected_outcome
    assert hint_fragment.lower() in message.lower()


def test_range_validation_is_inclusive_and_rejects_outside_values():
    assert validate_guess(1, 1, 20) == (True, None)
    assert validate_guess(20, 1, 20) == (True, None)
    assert validate_guess(21, 1, 20) == (False, "Choose a number from 1 to 20.")


def test_invalid_range_configuration_fails_loudly():
    with pytest.raises(ValueError, match="lower bound"):
        validate_guess(5, 10, 1)


def test_score_is_awarded_only_for_a_win_and_decreases_by_attempt():
    assert update_score(0, "Too High", 1) == 0
    assert update_score(0, "Too Low", 2) == 0
    assert update_score(0, "Win", 1) == 100
    assert update_score(15, "Win", 4) == 85


def test_late_win_has_a_minimum_score():
    assert update_score(0, "Win", 50) == 10


@pytest.mark.parametrize("outcome", ["", "Maybe", "too high"])
def test_unknown_score_outcome_fails_loudly(outcome):
    with pytest.raises(ValueError, match="Unknown outcome"):
        update_score(0, outcome, 1)


def test_zero_attempt_is_invalid_for_scoring():
    with pytest.raises(ValueError, match="at least 1"):
        update_score(0, "Win", 0)
