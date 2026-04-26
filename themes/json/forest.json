import svgwrite

def render(data):
    """
    Renders the Forest theme.
    Logic: Green shades for commits, dark background for empty days.
    """
    contributions = data["contributions"][-365:] if len(data["contributions"]) > 365 else data["contributions"]

    cols = 53
    rows = 7

    width = cols * 15 + 20
    height = rows * 15 + 40

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#0d1f0d"))

    box_size = 12
    gap = 3
    start_x = 10
    start_y = 10

    max_count = max((d["count"] for d in contributions), default=0)

    for i, day in enumerate(contributions):
        count = day["count"]
        col = i // rows
        row = i % rows
        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        if count == 0:
            fill_color = "#1a2e1a"
            stroke_color = "#0d1f0d"
        else:
            intensity = count / max_count if max_count > 0 else 0
            if intensity < 0.33:
                fill_color = "#2d5a27"
            elif intensity < 0.66:
                fill_color = "#4caf50"
            else:
                fill_color = "#a8d5a2"
            stroke_color = "#0d1f0d"

        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(box_size, box_size),
                fill=fill_color,
                stroke=stroke_color,
                stroke_width=0.7,
                rx=2,
                ry=2,
            )
        )

    # Legend
    legend_y = height - 14
    legend_x = 10
    legend_box = 9

    def legend_entry(x, label, color):
        dwg.add(
            dwg.rect(
                insert=(x, legend_y - legend_box + 2),
                size=(legend_box, legend_box),
                fill=color,
                stroke="#0d1f0d",
                stroke_width=0.6,
                rx=1,
                ry=1,
            )
        )
        dwg.add(
            dwg.text(
                label,
                insert=(x + legend_box + 4, legend_y + 1),
                fill="#c8e6c9",
                font_size=9,
                font_family="Segoe UI, Ubuntu, sans-serif",
            )
        )

    legend_entry(legend_x, "Empty", "#1a2e1a")
    legend_entry(legend_x + 80, "Growth", "#4caf50")
    legend_entry(legend_x + 160, "Canopy", "#a8d5a2")

    return dwg.tostring()
