from ai import description_generator


def _sample_profile():
    return {
        "username": "devuser",
        "total_commits": 420,
        "public_repos": 18,
        "followers": 73,
        "total_stars": 156,
        "top_languages": [("Python", 10), ("TypeScript", 6), ("Go", 2)],
        "contributions": [
            {"date": "2026-01-01", "count": 3},
            {"date": "2026-01-02", "count": 0},
            {"date": "2026-01-03", "count": 5},
        ],
    }


def test_create_description_prompt_includes_core_context():
    prompt = description_generator.create_description_prompt(
        _sample_profile(),
        theme_name="Space",
        tone="creative",
    )

    assert "Theme selected in app: Space" in prompt
    assert "Tone: creative" in prompt
    assert "Total commits: 420" in prompt
    assert "Top languages: Python, TypeScript, Go" in prompt


def test_fallback_description_mentions_theme_and_user():
    text = description_generator.get_fallback_description(
        _sample_profile(),
        theme_name="Cyberpunk",
        tone="funny",
    )

    assert "devuser" in text
    assert "Cyberpunk" in text


def test_generate_description_uses_fallback_when_providers_unavailable(monkeypatch):
    monkeypatch.setattr(description_generator, "openai_client", None)
    monkeypatch.setattr(description_generator, "GEMINI_API_KEY", None)

    result = description_generator.generate_github_description(
        _sample_profile(),
        theme_name="Ocean",
        tone="professional",
    )

    assert result["success"] is True
    assert result["source"] == "fallback"
    assert result["tone"] == "professional"
    assert "Ocean" in result["description"]


def test_invalid_tone_defaults_to_professional(monkeypatch):
    monkeypatch.setattr(description_generator, "openai_client", None)
    monkeypatch.setattr(description_generator, "GEMINI_API_KEY", None)

    result = description_generator.generate_github_description(
        _sample_profile(),
        theme_name="Glass",
        tone="wild",
    )

    assert result["tone"] == "professional"
