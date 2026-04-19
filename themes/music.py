import svgwrite

def render(data):
    """
    Renders the Music theme (Audio Waveform).
    """

    contributions = data['contributions'][-100:] if data.get('contributions') else []

    width = 800
    height = 400

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#0d0d0d"))

    # Title (use symbol, not emoji)
    dwg.add(dwg.text(
        "♪ Music Wave",
        insert=(width / 2, 30),
        text_anchor="middle",
        fill="#ff00cc",
        font_size="24px",
        font_family="Arial"
    ))

    # No data case
    if not contributions:
        dwg.add(dwg.text(
            "No Data",
            insert=(width / 2, height / 2),
            text_anchor="middle",
            fill="white",
            font_size="20px"
        ))
        return dwg.tostring()

    num_bars = len(contributions)
    bar_width = max(1, (width - 40) / num_bars - 2)

    center_y = height / 2
    max_amp = height / 2 - 20

    max_commits = max(d['count'] for d in contributions) or 1

    start_x = 20

    # Corner accents (SVG-safe symbols)
    dwg.add(dwg.text("♬", insert=(10, 30), fill="#9d00ff", font_size="16px"))
    dwg.add(dwg.text("♫", insert=(width - 40, 30), fill="#00f5ff", font_size="16px"))

    for i, day in enumerate(contributions):
        count = day['count']

        normalized = count / max_commits
        amp = normalized * max_amp + 5

        x = start_x + i * (bar_width + 2)

        # Color logic
        if count == 0:
            color = "#444444"
        elif count < 3:
            color = "#ff00cc"
        elif count < 6:
            color = "#9d00ff"
        else:
            color = "#00f5ff"

        # Bar
        dwg.add(dwg.rect(
            insert=(x, center_y - amp),
            size=(bar_width, amp * 2),
            fill=color,
            rx=bar_width / 2,
            ry=bar_width / 2
        ))

        # Add note only for high activity (clean + meaningful)
        if count > 5:
            dwg.add(dwg.text(
                "♪",
                insert=(x, center_y - amp - 6),
                fill="#ff00cc",
                font_size="10px"
            ))

    return dwg.tostring()