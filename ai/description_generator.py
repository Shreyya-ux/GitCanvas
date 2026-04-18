"""
AI description generator for GitCanvas GitHub stats.
Generates short, theme-aware textual summaries with OpenAI/Gemini and a safe fallback.
"""

from __future__ import annotations

import re
from typing import Any

from config.settings import get_settings
from utils.logger import setup_logger

try:
    import google.generativeai as genai  # type: ignore

    _HAS_GENAI = True
except Exception:
    genai = None
    _HAS_GENAI = False

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


logger = setup_logger(__name__)


SUPPORTED_TONES = {"professional", "funny", "creative"}


_cfg = get_settings()
OPENAI_API_KEY = _cfg.openai_api_key_value()
GEMINI_API_KEY = _cfg.gemini_api_key_value()

openai_client = None
if OPENAI_API_KEY and OpenAI:
    try:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as exc:
        logger.warning(f"Failed to initialize OpenAI client: {exc}")

if GEMINI_API_KEY and _HAS_GENAI:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as exc:
        logger.warning(f"Failed to configure Gemini client: {exc}")


def _normalize_tone(tone: str | None) -> str:
    if not tone:
        return "professional"
    normalized = tone.strip().lower()
    if normalized not in SUPPORTED_TONES:
        return "professional"
    return normalized


def _normalize_top_languages(raw_languages: Any) -> list[str]:
    languages: list[str] = []

    if not isinstance(raw_languages, list):
        return languages

    for entry in raw_languages:
        if isinstance(entry, dict):
            name = entry.get("name")
            if isinstance(name, str) and name.strip():
                languages.append(name.strip())
        elif isinstance(entry, (list, tuple)) and entry:
            name = str(entry[0]).strip()
            if name:
                languages.append(name)

    return languages[:5]


def _active_contribution_days(contributions: Any) -> int:
    if not isinstance(contributions, list):
        return 0

    active_days = 0
    for item in contributions:
        if isinstance(item, dict) and int(item.get("count", 0) or 0) > 0:
            active_days += 1
    return active_days


def _clean_text(value: str) -> str:
    cleaned = value.strip().strip('"').strip("'")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def create_description_prompt(profile_data: dict[str, Any], theme_name: str, tone: str = "professional") -> str:
    """Create a compact prompt describing profile stats with theme context."""
    normalized_tone = _normalize_tone(tone)

    username = profile_data.get("username", "developer")
    commits = int(profile_data.get("total_commits", 0) or 0)
    repos = int(profile_data.get("public_repos", 0) or 0)
    followers = int(profile_data.get("followers", 0) or 0)
    stars = int(profile_data.get("total_stars", 0) or 0)

    languages = _normalize_top_languages(profile_data.get("top_languages", []))
    languages_str = ", ".join(languages[:3]) if languages else "multiple languages"

    active_days = _active_contribution_days(profile_data.get("contributions", []))

    tone_guidelines = {
        "professional": "Use a clear, polished and insightful tone.",
        "funny": "Use light and friendly humor without being rude.",
        "creative": "Use vivid and imaginative wording while staying readable.",
    }

    return f"""
Write a short GitHub profile description in 3 to 4 sentences.

Username: {username}
Theme selected in app: {theme_name}
Total commits: {commits}
Public repositories: {repos}
Followers: {followers}
Total stars: {stars}
Top languages: {languages_str}
Active contribution days (in loaded dataset): {active_days}
Tone: {normalized_tone}

Rules:
- Mention the selected theme naturally.
- Include at least two concrete stats from above.
- Keep it under 95 words.
- Avoid bullet points and hashtags.
- {tone_guidelines[normalized_tone]}
Return only the description text.
""".strip()


def generate_description_with_openai(profile_data: dict[str, Any], theme_name: str, tone: str = "professional") -> str:
    """Generate description via OpenAI Chat Completions."""
    if not openai_client:
        raise ValueError("OpenAI is not configured")

    prompt = create_description_prompt(profile_data, theme_name, tone)
    normalized_tone = _normalize_tone(tone)

    temperature = {
        "professional": 0.5,
        "funny": 0.8,
        "creative": 0.9,
    }[normalized_tone]

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You summarize GitHub profiles accurately and engagingly.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=180,
        temperature=temperature,
    )

    content = response.choices[0].message.content or ""
    cleaned = _clean_text(content)
    if not cleaned:
        raise ValueError("OpenAI returned empty description")
    return cleaned


def generate_description_with_gemini(profile_data: dict[str, Any], theme_name: str, tone: str = "professional") -> str:
    """Generate description via Gemini."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not configured")
    if not _HAS_GENAI:
        raise ImportError("google.generativeai is not installed")

    prompt = create_description_prompt(profile_data, theme_name, tone)
    normalized_tone = _normalize_tone(tone)

    temperature = {
        "professional": 0.5,
        "funny": 0.8,
        "creative": 0.9,
    }[normalized_tone]

    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=180,
    )

    last_error: Exception | None = None
    for model_name in ("gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt, generation_config=generation_config)
            content = getattr(response, "text", "") or ""
            cleaned = _clean_text(content)
            if cleaned:
                return cleaned
        except Exception as exc:
            last_error = exc

    raise ValueError(f"Gemini returned empty description or unsupported model. Last error: {last_error}")


def get_fallback_description(profile_data: dict[str, Any], theme_name: str, tone: str = "professional") -> str:
    """Return a deterministic local fallback description when LLM calls fail."""
    normalized_tone = _normalize_tone(tone)

    username = profile_data.get("username", "This developer")
    commits = int(profile_data.get("total_commits", 0) or 0)
    repos = int(profile_data.get("public_repos", 0) or 0)
    followers = int(profile_data.get("followers", 0) or 0)
    stars = int(profile_data.get("total_stars", 0) or 0)

    languages = _normalize_top_languages(profile_data.get("top_languages", []))
    primary_lang = languages[0] if languages else "multiple languages"

    if normalized_tone == "funny":
        return (
            f"{username} is running a {theme_name} coding universe where {commits} commits and "
            f"{repos} repos keep the plot moving. Their favorite tool seems to be {primary_lang}, "
            f"with {stars} stars and {followers} followers cheering from the sidelines."
        )

    if normalized_tone == "creative":
        return (
            f"In the {theme_name} palette, {username}'s GitHub story glows through {commits} commits "
            f"and {repos} public repositories. {primary_lang} leads the rhythm, while {stars} stars and "
            f"{followers} followers reflect the reach of their craft."
        )

    return (
        f"{username} shows consistent development activity with {commits} commits across {repos} public repositories. "
        f"Using {primary_lang} as a key language, the profile has gathered {stars} stars and {followers} followers. "
        f"The selected {theme_name} theme highlights this contribution pattern clearly."
    )


def generate_github_description(
    profile_data: dict[str, Any],
    theme_name: str,
    tone: str = "professional",
) -> dict[str, Any]:
    """
    Generate a theme-aware GitHub description with resilient provider fallback.

    Returns metadata containing source provider and final description text.
    """
    normalized_tone = _normalize_tone(tone)
    description_text: str | None = None
    source = "fallback"

    try:
        if openai_client:
            try:
                description_text = generate_description_with_openai(profile_data, theme_name, normalized_tone)
                source = "openai"
            except Exception as exc:
                logger.warning(f"OpenAI description generation failed: {exc}")

        if not description_text and GEMINI_API_KEY and _HAS_GENAI:
            try:
                description_text = generate_description_with_gemini(profile_data, theme_name, normalized_tone)
                source = "gemini"
            except Exception as exc:
                logger.warning(f"Gemini description generation failed: {exc}")

        if not description_text:
            description_text = get_fallback_description(profile_data, theme_name, normalized_tone)
            source = "fallback"

        return {
            "success": True,
            "description": description_text,
            "source": source,
            "tone": normalized_tone,
            "theme": theme_name,
            "username": profile_data.get("username", "developer"),
        }

    except Exception as exc:
        logger.error(f"Unexpected description generation error: {exc}")
        return {
            "success": False,
            "description": get_fallback_description(profile_data, theme_name, normalized_tone),
            "source": "fallback",
            "tone": normalized_tone,
            "theme": theme_name,
            "username": profile_data.get("username", "developer"),
            "error": str(exc),
        }
