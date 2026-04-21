# tests/test_stats_card.py
import pytest
from generators.stats_card import draw_stats_card


def test_stats_card_returns_string(mock_user_data, show_options_all):
    result = draw_stats_card(mock_user_data, "Default", show_options_all)
    assert isinstance(result, str)


def test_stats_card_is_valid_svg(mock_user_data, show_options_all):
    result = draw_stats_card(mock_user_data, "Default", show_options_all)
    assert result.strip().startswith("<svg") or "svg" in result
    assert "</svg>" in result


def test_stats_card_contains_username(mock_user_data, show_options_all):
    result = draw_stats_card(mock_user_data, "Default", show_options_all)
    assert "testuser" in result


def test_stats_card_contains_star_value(mock_user_data, show_options_all):
    result = draw_stats_card(mock_user_data, "Default", show_options_all)
    assert "120" in result


def test_stats_card_all_themes(mock_user_data, show_options_all):
    from themes.styles import THEMES
    for theme_name in THEMES:
        result = draw_stats_card(mock_user_data, theme_name, show_options_all)
        assert "</svg>" in result, f"Theme '{theme_name}' did not produce valid SVG"


def test_stats_card_compact_mode(mock_user_data, show_options_all):
    result = draw_stats_card(mock_user_data, "Default", show_options_all, compact=True)
    assert isinstance(result, str)
    assert "</svg>" in result


def test_stats_card_hidden_stats(mock_user_data, show_options_none):
    result = draw_stats_card(mock_user_data, "Default", show_options_none)
    assert isinstance(result, str)
    assert "</svg>" in result


def test_stats_card_empty_data():
    result = draw_stats_card({}, "Default", {"stars": True, "commits": True, "repos": True, "followers": True})
    assert isinstance(result, str)
    assert "</svg>" in result