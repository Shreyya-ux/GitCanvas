from themes.styles import get_all_themes


def test_music_theme_is_registered():
    themes = get_all_themes()
    assert "Music" in themes


def test_music_theme_has_tags_for_sidebar_filters():
    themes = get_all_themes()
    music_theme = themes["Music"]
    tags = music_theme.get("tags", [])
    assert "music" in [tag.lower() for tag in tags]
