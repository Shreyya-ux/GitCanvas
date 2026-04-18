# utils/error_card.py
# Resolves Issue #165 — visual fallback SVG card for API errors

import svgwrite


def draw_error_card(error_type: str = "rate_limit", username: str = "user", message: str = "") -> str:
    WIDTH, HEIGHT = 450, 160

    aliases = {
        "invalid_user": "user_not_found",
        "rate_limit": "rate_limited",
        "unknown": "api_error",
    }
    resolved_error_type = aliases.get(error_type, error_type)

    config = {
        "rate_limited": {
            "icon":    "⏳",
            "title":   "Rate Limited",
            "line1":   "GitHub's API limit was hit for this session.",
            "line2":   "Add a GITHUB_TOKEN in the sidebar or .env",
            "line3":   "to increase the limit from 60 → 5,000 req/hr.",
            "bg":      "#161b22",
            "border":  "#f0883e",
            "title_c": "#f0883e",
            "text_c":  "#c9d1d9",
        },
        "user_not_found": {
            "icon":    "❌",
            "title":   "User Not Found",
            "line1":   "No GitHub account exists for this username.",
            "line2":   f'Username: "{username}"',
            "line3":   "",
            "bg":      "#161b22",
            "border":  "#f85149",
            "title_c": "#f85149",
            "text_c":  "#c9d1d9",
        },
        "api_error": {
            "icon":    "⚠️",
            "title":   "GitHub API Error",
            "line1":   message or "Could not load GitHub profile data.",
            "line2":   "Please try again in a few minutes.",
            "line3":   "",
            "bg":      "#161b22",
            "border":  "#e3b341",
            "title_c": "#e3b341",
            "text_c":  "#c9d1d9",
        },
    }

    c = config.get(resolved_error_type, config["api_error"])

    dwg = svgwrite.Drawing(size=(WIDTH, HEIGHT))
    dwg.viewbox(0, 0, WIDTH, HEIGHT)

    # Background
    dwg.add(dwg.rect(
        insert=(0, 0), size=(WIDTH, HEIGHT),
        rx=12, ry=12,
        fill=c["bg"], stroke=c["border"], stroke_width=2
    ))

    # Top accent bar
    dwg.add(dwg.rect(
        insert=(0, 0), size=(WIDTH, 4),
        rx=2, ry=2, fill=c["border"]
    ))

    # Icon
    dwg.add(dwg.text(
        c["icon"],
        insert=(20, 42),
        font_size=22,
        font_family="Segoe UI Emoji, sans-serif"
    ))

    # Title
    dwg.add(dwg.text(
        c["title"],
        insert=(52, 42),
        fill=c["title_c"],
        font_size=14,
        font_family="Segoe UI, Ubuntu, sans-serif",
        font_weight="bold"
    ))

    # Divider
    dwg.add(dwg.line(
        start=(20, 55), end=(WIDTH - 20, 55),
        stroke=c["border"], stroke_width=0.8, opacity=0.5
    ))

    # Body lines
    for i, line in enumerate([c["line1"], c["line2"], c["line3"]]):
        if line:
            dwg.add(dwg.text(
                line,
                insert=(20, 78 + i * 22),
                fill=c["text_c"],
                font_size=11,
                font_family="Segoe UI, Ubuntu, sans-serif",
                opacity=0.9
            ))

    # Footer
    dwg.add(dwg.text(
        "GitCanvas — gitcanvas-dm.streamlit.app",
        insert=(WIDTH - 20, HEIGHT - 12),
        fill=c["text_c"],
        font_size=9,
        font_family="Segoe UI, Ubuntu, sans-serif",
        text_anchor="end",
        opacity=0.4
    ))

    return dwg.tostring()