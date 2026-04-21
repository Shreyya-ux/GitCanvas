# tests/test_repo_card.py
import pytest
from generators.repo_card import draw_repo_card


def test_repo_card_returns_string(mock_user_data):
    result = draw_repo_card(mock_user_data)
    assert isinstance(result, str)


def test_repo_card_is_valid_svg(mock_user_data):
    result = draw_repo_card(mock_user_data)
    assert "</svg>" in result


def test_repo_card_contains_repo_name(mock_user_data):
    result = draw_repo_card(mock_user_data)
    assert "awesome-project" in result


def test_repo_card_sort_by_stars(mock_user_data):
    result = draw_repo_card(mock_user_data, sort_by="stars")
    assert "</svg>" in result


def test_repo_card_sort_by_forks(mock_user_data):
    result = draw_repo_card(mock_user_data, sort_by="forks")
    assert "</svg>" in result


def test_repo_card_limit(mock_user_data):
    result = draw_repo_card(mock_user_data, limit=1)
    assert isinstance(result, str)
    assert "</svg>" in result


def test_repo_card_compact_mode(mock_user_data):
    result = draw_repo_card(mock_user_data, compact=True)
    assert isinstance(result, str)
    assert "</svg>" in result


def test_repo_card_empty_repos():
    result = draw_repo_card({"top_repos": []})
    assert isinstance(result, str)
    assert "</svg>" in result