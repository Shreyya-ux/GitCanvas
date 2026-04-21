import svgwrite
from themes.styles import THEMES
from .svg_base import create_svg_base, draw_card_background, draw_divider_line

def draw_repo_card(data, theme_name="Default", custom_colors=None, sort_by="stars", limit=5, compact=False):
    """
    Generates the Top Repositories Card SVG.
    data: dict with 'top_repos' list containing repo data
    theme_name: string key from THEMES
    sort_by: sorting criteria used (for display purposes)
    limit: number of repos displayed
    """
    repos = data.get("top_repos", [])
    
    # Apply sorting based on user selection
    if repos and len(repos) > 0 and "name" in repos[0]:
        if sort_by == "stars":
            repos = sorted(repos, key=lambda x: x.get("stars", 0), reverse=True)
        elif sort_by == "forks":
            repos = sorted(repos, key=lambda x: x.get("forks", 0), reverse=True)
        elif sort_by == "updated":
            repos = sorted(repos, key=lambda x: x.get("updated_at", ""), reverse=True)
    
    # Apply limit
    repos = repos[:limit]

    # ── Compact Layout 
    if compact:
        compact_width  = 300
        compact_height = 30 + (len(repos) * 28) + 10
        
        from themes.styles import THEMES
        if isinstance(theme_name, dict):
            theme = theme_name.copy()
        else:
            theme = THEMES.get(theme_name, THEMES["Default"]).copy()
            if custom_colors:
                theme.update(custom_colors)

        bg_col     = theme.get("bg_color",     "#0d1117")
        border_col = theme.get("border_color", "#30363d")
        title_col  = theme.get("title_color",  "#58a6ff")
        text_col   = theme.get("text_color",   "#c9d1d9")
        icon_col   = theme.get("icon_color",   "#8b949e")
        font       = theme.get("font_family",  "Segoe UI, Ubuntu, Sans-Serif")

        c_dwg = svgwrite.Drawing(size=(compact_width, compact_height))
        c_dwg.viewbox(0, 0, compact_width, compact_height)

        # Background
        c_dwg.add(c_dwg.rect(
            insert=(0, 0), size=(compact_width, compact_height),
            rx=10, ry=10,
            fill=bg_col, stroke=border_col, stroke_width=1.5
        ))

        # Title
        sort_labels = {"stars": "Top Repos ⭐", "forks": "Top Repos 🔱", "updated": "Top Repos 🕐"}
        c_dwg.add(c_dwg.text(
            sort_labels.get(sort_by, "Top Repos"),
            insert=(12, 20),
            fill=title_col, font_size=10,
            font_family=font, font_weight="bold"
        ))

        # Divider
        c_dwg.add(c_dwg.line(
            start=(12, 25), end=(compact_width - 12, 25),
            stroke=border_col, stroke_width=0.8
        ))

        # Repo rows
        for i, repo in enumerate(repos[:5]):
            y = 38 + i * 28
            name = repo.get("name", "Unknown")[:22]
            stars = repo.get("stars", 0)

            # Repo name
            c_dwg.add(c_dwg.text(
                name,
                insert=(12, y),
                fill=text_col, font_size=9,
                font_family=font, font_weight="bold"
            ))

            # Star dot + count
            c_dwg.add(c_dwg.circle(
                center=(compact_width - 45, y - 4),
                r=3, fill="#FFD700", opacity=0.9
            ))
            c_dwg.add(c_dwg.text(
                f"{stars:,}",
                insert=(compact_width - 38, y),
                fill=icon_col, font_size=8,
                font_family=font
            ))

            # Language
            lang = repo.get("language") or ""
            if lang:
                c_dwg.add(c_dwg.text(
                    lang[:12],
                    insert=(12, y + 12),
                    fill=icon_col, font_size=7,
                    font_family=font, opacity=0.7
                ))

            # Separator
            if i < len(repos) - 1:
                c_dwg.add(c_dwg.line(
                    start=(12, y + 18), end=(compact_width - 12, y + 18),
                    stroke=border_col, stroke_width=0.5, opacity=0.4
                ))

        return c_dwg.tostring()
    # ── End Compact Layout ────────────────────────────────────────────────
    
    if not repos:
        # Return empty card with message
        repos = [{"name": "No repositories found", "description": "Try a different username", "language": "N/A", "stars": 0, "forks": 0}]
    
    width = 500
    # Dynamic height based on number of repos
    header_height = 50
    repo_height = 75  # Height per repo item
    footer_height = 20
    height = header_height + (len(repos) * repo_height) + footer_height
    
    # Create title based on sort criteria
    sort_labels = {
        "stars": "Most Starred",
        "forks": "Most Forked", 
        "updated": "Recently Updated"
    }
    title = f"{sort_labels.get(sort_by, 'Top')} Repositories"
    
    dwg, theme = create_svg_base(theme_name, custom_colors, width, height, title)
    
    font_family = theme["font_family"]
    text_color = theme["text_color"]
    title_color = theme["title_color"]
    icon_color = theme["icon_color"]
    border_color = theme["border_color"]
    
    # Starting Y position for repos
    start_y = 65
    
    for i, repo in enumerate(repos):
        y = start_y + (i * repo_height)
        
        # Repo name (bold, larger)
        dwg.add(dwg.text(
            repo.get("name", "Unknown")[:30],  # Truncate long names
            insert=(20, y),
            fill=title_color,
            font_size=16,
            font_family=font_family,
            font_weight="bold"
        ))
        
        # Description (smaller, truncated)
        desc = repo.get("description", "No description") or "No description"
        desc = desc[:50] + "..." if len(desc) > 50 else desc
        dwg.add(dwg.text(
            desc,
            insert=(20, y + 18),
            fill=text_color,
            font_size=11,
            font_family=font_family,
            opacity=0.8
        ))
        
        # Language badge (if available)
        language = repo.get("language", "Unknown") or "Unknown"
        if language != "Unknown":
            # Language color dot
            lang_colors = {
                "Python": "#3776ab",
                "JavaScript": "#f7df1e",
                "TypeScript": "#3178c6",
                "Java": "#b07219",
                "C++": "#f34b7d",
                "C": "#555555",
                "Go": "#00add8",
                "Rust": "#dea584",
                "Ruby": "#701516",
                "PHP": "#4F5D95",
                "Swift": "#ffac45",
                "Kotlin": "#A97BFF",
                "HTML": "#e34c26",
                "CSS": "#563d7c",
                "Shell": "#89e051",
                "R": "#198CE7",
                "Scala": "#c22d40",
                "Dart": "#00B4AB",
                "Elixir": "#6e4a7e",
                "Clojure": "#db5855",
                "Haskell": "#5e5086",
                "Lua": "#000080",
                "Perl": "#0298c3",
                "Julia": "#a270ba",
                "Erlang": "#b83998",
                "Objective-C": "#438eff",
                "CoffeeScript": "#244776",
                "Vim script": "#199f4b",
                "TeX": "#3D6117",
                "Jupyter Notebook": "#DA5B0B"
            }
            lang_color = lang_colors.get(language, icon_color)
            
            dwg.add(dwg.circle(
                center=(30, y + 38),
                r=5,
                fill=lang_color
            ))
            
            dwg.add(dwg.text(
                language,
                insert=(42, y + 42),
                fill=text_color,
                font_size=11,
                font_family=font_family
            ))
        
        # Stars count (right side)
        stars = repo.get("stars", 0)
        stars_x = width - 120
        
        # Star icon (simple polygon)
        star_points = []
        for j in range(10):
            angle = j * 36 - 90  # Start from top
            if j % 2 == 0:
                r = 6  # Outer radius
            else:
                r = 3  # Inner radius
            x = stars_x + r * 0.9 * (j % 2)  # Simplified star as small shape
            y_star = y + 35 + r * 0.5
            # Use a simple circle for star to keep it clean
        dwg.add(dwg.circle(
            center=(stars_x, y + 35),
            r=4,
            fill="#FFD700",  # Gold color for stars
            opacity=0.9
        ))
        
        dwg.add(dwg.text(
            f"{stars:,}",
            insert=(stars_x + 12, y + 39),
            fill=text_color,
            font_size=12,
            font_family=font_family,
            font_weight="bold"
        ))
        
        # Forks count
        forks = repo.get("forks", 0)
        forks_x = width - 50
        
        # Fork icon (simple Y shape using path)
        fork_path = f"M {forks_x} {y + 32} L {forks_x} {y + 38} M {forks_x} {y + 35} L {forks_x - 4} {y + 30} M {forks_x} {y + 35} L {forks_x + 4} {y + 30}"
        dwg.add(dwg.path(
            d=fork_path,
            stroke=icon_color,
            stroke_width=2,
            fill="none"
        ))
        
        dwg.add(dwg.text(
            f"{forks:,}",
            insert=(forks_x + 10, y + 39),
            fill=text_color,
            font_size=12,
            font_family=font_family
        ))
        
        # Separator line between repos (except for last one)
        if i < len(repos) - 1:
            draw_divider_line(dwg, 20, y + repo_height - 8, width - 20, y + repo_height - 8, theme)
    
    return dwg.tostring()
