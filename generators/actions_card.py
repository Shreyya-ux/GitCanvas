import svgwrite
from themes.styles import THEMES
from .svg_base import create_svg_base, CSS_ANIMATIONS


def draw_actions_card(data, theme_name="Default", custom_colors=None, animations_enabled=True):
    """
    Generates the GitHub Actions Stats Card SVG.
    
    Args:
        data: dict with actions stats (total_workflows, total_runs, successful_runs, failed_runs, success_rate, recent_runs)
        theme_name: string key from THEMES
        custom_colors: dict with color overrides
        animations_enabled: bool to enable/disable CSS animations
    
    Returns:
        SVG string
    """
    # Handle theme - convert string to dict if needed
    if isinstance(theme_name, dict):
        theme = theme_name.copy()
    else:
        theme = THEMES.get(theme_name, THEMES["Default"]).copy()
        if custom_colors:
            theme.update(custom_colors)
    
    # Get stats from data
    total_workflows = data.get('total_workflows', 0) if data else 0
    total_runs = data.get('total_runs', 0) if data else 0
    successful_runs = data.get('successful_runs', 0) if data else 0
    failed_runs = data.get('failed_runs', 0) if data else 0
    success_rate = data.get('success_rate', 0) if data else 0
    recent_runs = data.get('recent_runs', []) if data else []
    
    width = 500
    base_height = 60
    stat_item_height = 30
    recent_section_height = 120
    
    # Calculate height based on recent runs (show max 4)
    shown_recent_runs = min(len(recent_runs), 4)
    recent_run_height = 20 * shown_recent_runs if shown_recent_runs > 0 else 0
    
    height = base_height + (4 * stat_item_height) + recent_section_height + recent_run_height + 40
    
    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    
    # Add CSS animations if enabled
    if animations_enabled:
        dwg.defs.add(dwg.style(CSS_ANIMATIONS))
    
    # Background
    dwg.add(dwg.rect(
        insert=(0, 0),
        size=("100%", "100%"),
        rx=10,
        ry=10,
        fill=theme.get("bg_color", "#0d1117"),
        stroke=theme.get("border_color", "#30363d"),
        stroke_width=2
    ))
    
    # Title
    title_y = 25
    dwg.add(dwg.text(
        "Github Actions",
        insert=(20, title_y),
        font_size=18,
        font_weight="bold",
        fill=theme.get("title_color", "#58a6ff"),
        font_family="Arial, sans-serif"
    ))
    
    # GitHub Actions icon (simple)
    icon_x = width - 35
    icon_y = title_y - 15
    
    # Create a simple workflow icon
    dwg.add(dwg.circle(
        center=(icon_x, icon_y),
        r=8,
        fill="none",
        stroke=theme.get("title_color", "#58a6ff"),
        stroke_width=1.5
    ))
    dwg.add(dwg.circle(
        center=(icon_x - 12, icon_y + 8),
        r=5,
        fill="none",
        stroke=theme.get("title_color", "#58a6ff"),
        stroke_width=1.5
    ))
    dwg.add(dwg.circle(
        center=(icon_x + 12, icon_y + 8),
        r=5,
        fill="none",
        stroke=theme.get("title_color", "#58a6ff"),
        stroke_width=1.5
    ))
    dwg.add(dwg.line(
        start=(icon_x, icon_y + 8),
        end=(icon_x - 12, icon_y + 8),
        stroke=theme.get("title_color", "#58a6ff"),
        stroke_width=1.5
    ))
    dwg.add(dwg.line(
        start=(icon_x, icon_y + 8),
        end=(icon_x + 12, icon_y + 8),
        stroke=theme.get("title_color", "#58a6ff"),
        stroke_width=1.5
    ))
    
    # Stats section
    y_pos = 55
    text_color = theme.get("text_color", "#c9d1d9")
    
    # Helper function to add stat rows
    def add_stat_row(y, label, value, value_color=None):
        if value_color is None:
            value_color = theme.get("icon_color", "#58a6ff")
        
        dwg.add(dwg.text(
            label,
            insert=(25, y),
            font_size=12,
            fill=text_color,
            font_family="Arial, sans-serif"
        ))
        
        dwg.add(dwg.text(
            str(value),
            insert=(width - 50, y),
            font_size=12,
            font_weight="bold",
            fill=value_color,
            font_family="Arial, sans-serif",
            text_anchor="end"
        ))
    
    # Add stat rows
    add_stat_row(y_pos, "Total Workflows:", total_workflows)
    y_pos += stat_item_height
    
    add_stat_row(y_pos, "Total Runs:", total_runs)
    y_pos += stat_item_height
    
    add_stat_row(y_pos, "Successful:", successful_runs,
                 value_color=theme.get("success_color", "#238636") or "#238636")
    y_pos += stat_item_height
    
    add_stat_row(y_pos, "Failed:", failed_runs,
                 value_color=theme.get("fail_color", "#f85149") or "#f85149")
    y_pos += stat_item_height
    
    # Success rate with progress bar
    bar_y = y_pos + 5
    bar_width = width - 50
    bar_height = 6
    
    dwg.add(dwg.text(
        "Success Rate:",
        insert=(25, y_pos),
        font_size=12,
        fill=text_color,
        font_family="Arial, sans-serif"
    ))
    
    dwg.add(dwg.text(
        f"{success_rate}%",
        insert=(width - 25, y_pos),
        font_size=12,
        font_weight="bold",
        fill=theme.get("title_color", "#58a6ff"),
        font_family="Arial, sans-serif",
        text_anchor="end"
    ))
    
    # Progress bar background
    dwg.add(dwg.rect(
        insert=(25, bar_y),
        size=(bar_width, bar_height),
        rx=3,
        ry=3,
        fill=theme.get("border_color", "#30363d")
    ))
    
    # Progress bar fill
    if success_rate > 0:
        fill_width = (bar_width * success_rate) / 100
        
        # Color based on success rate
        if success_rate >= 90:
            bar_color = theme.get("success_color", "#238636") or "#238636"
        elif success_rate >= 70:
            bar_color = theme.get("warning_color", "#d29922") or "#d29922"
        else:
            bar_color = theme.get("fail_color", "#f85149") or "#f85149"
        
        dwg.add(dwg.rect(
            insert=(25, bar_y),
            size=(fill_width, bar_height),
            rx=3,
            ry=3,
            fill=bar_color
        ))
    
    # Recent runs section (if available)
    if recent_runs:
        y_pos += stat_item_height + 10
        
        dwg.add(dwg.text(
            "Recent Runs",
            insert=(25, y_pos),
            font_size=12,
            font_weight="bold",
            fill=theme.get("title_color", "#58a6ff"),
            font_family="Arial, sans-serif"
        ))
        
        y_pos += 18
        
        # Show max 4 recent runs
        for i, run in enumerate(recent_runs[:4]):
            if i >= 4:
                break
            
            repo = run.get('repo', 'Unknown')
            workflow = run.get('workflow', 'Unknown')
            conclusion = run.get('conclusion', 'unknown')
            
            # Status color
            if conclusion == 'success':
                status_color = theme.get("success_color", "#238636") or "#238636"
                status_icon = "✓"
            elif conclusion == 'failure':
                status_color = theme.get("fail_color", "#f85149") or "#f85149"
                status_icon = "✗"
            else:
                status_color = theme.get("icon_color", "#58a6ff") or "#58a6ff"
                status_icon = "○"
            
            # Status indicator
            dwg.add(dwg.circle(
                center=(25, y_pos - 4),
                r=3,
                fill=status_color
            ))
            
            # Workflow name
            workflow_text = f"{repo}/{workflow}"
            if len(workflow_text) > 40:
                workflow_text = workflow_text[:37] + "..."
            
            dwg.add(dwg.text(
                workflow_text,
                insert=(35, y_pos),
                font_size=10,
                fill=text_color,
                font_family="monospace"
            ))
            
            y_pos += 18
    
    # Footer note
    footer_y = height - 8
    dwg.add(dwg.text(
        "Powered by GitHub Actions API",
        insert=(width / 2, footer_y),
        font_size=8,
        fill=theme.get("border_color", "#30363d"),
        font_family="Arial, sans-serif",
        text_anchor="middle",
        opacity=0.6
    ))
    
    return dwg.tostring()
