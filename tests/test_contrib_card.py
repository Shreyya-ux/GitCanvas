from datetime import date, timedelta

from generators.contrib_card import draw_calendar_heatmap_card


def test_calendar_heatmap_returns_svg():
    today = date(2026, 4, 16)
    contributions = [
        {"date": (today - timedelta(days=index)).isoformat(), "count": (index % 6) + 1}
        for index in range(30)
    ]

    result = draw_calendar_heatmap_card(
        {"username": "testuser", "contributions": contributions},
        theme_name="Default",
        date_range={
            "start": (today - timedelta(days=365)).isoformat(),
            "end": today.isoformat(),
        },
    )

    assert isinstance(result, str)
    assert result.startswith("<svg")
    assert "viewBox=\"0 0 735 169\"" in result
    assert "testuser's Contribution Calendar" in result