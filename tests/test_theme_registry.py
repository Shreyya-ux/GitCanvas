from themes.styles import get_all_themes


def test_music_theme_is_registered():
    themes = get_all_themes()
    assert "Music" in themes


def test_music_theme_has_tags_for_sidebar_filters():
    themes = get_all_themes()
    music_theme = themes["Music"]
    tags = music_theme.get("tags", [])
    assert "music" in [tag.lower() for tag in tags]


def test_aurora_gradient_theme_is_registered_with_tags():
    themes = get_all_themes()
    assert "Aurora Gradient" in themes

    aurora_theme = themes["Aurora Gradient"]
    tags = aurora_theme.get("tags", [])
    assert "aurora" in [tag.lower() for tag in tags]
