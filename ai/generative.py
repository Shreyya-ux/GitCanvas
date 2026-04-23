"""
AI-powered generative functions for artistic profile descriptions and vibe analysis
Uses Google Gemini API with fallback heuristics
"""

from typing import List, Dict, Optional
from config.settings import get_settings
from utils.logger import setup_logger
import logging

try:
    import google.generativeai as genai
    _HAS_GENAI = True
except Exception:
    genai = None
    _HAS_GENAI = False

logger = setup_logger(__name__)

# Get API keys
_cfg = get_settings()
GEMINI_API_KEY = _cfg.gemini_api_key_value()

# Initialize Gemini
if GEMINI_API_KEY and _HAS_GENAI:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to configure Gemini for generative AI: {e}")


def generate_artistic_caption(username: str, total_commits: int, top_language: str) -> str:
    """
    Generate a poetic or cool artistic caption describing a developer's coding style.
    
    Uses Google Gemini API to create dynamic, personalized descriptions.
    Falls back to template-based generation if API is unavailable.
    
    Args:
        username: GitHub username
        total_commits: Total number of commits by the user
        top_language: Primary programming language
        
    Returns:
        Artistic caption string describing the user's coding journey
    """
    # Try Gemini API if available
    if GEMINI_API_KEY and _HAS_GENAI and genai:
        try:
            return _generate_caption_with_gemini(username, total_commits, top_language)
        except Exception as e:
            logger.warning(f"Gemini API failed for artistic caption: {e}, using fallback")
    
    # Fallback to template-based generation
    return _generate_caption_fallback(username, total_commits, top_language)


def _generate_caption_with_gemini(username: str, total_commits: int, top_language: str) -> str:
    """
    Generate artistic caption using Google Gemini API
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Create a single poetic or artistic one-line caption describing a developer's coding journey.

Developer Profile:
- Username: {username}
- Total Commits: {total_commits}
- Primary Language: {top_language}

Generate ONE creative, artistic caption that's poetic or inspirational. Examples:
- "A {top_language} artisan sculpting logic with {total_commits} strokes of genius"
- "Every {total_commits} commit is a verse in {username}'s code poetry"
- "{username}: Writing dreams in {top_language}, one commit at a time"
- "The digital odyssey of {username} - {total_commits} commits, infinite possibilities"

Requirements:
- Exactly ONE line
- Poetic, artistic, or inspirational tone
- Reference the language and/or commit count naturally
- Be creative and personalized

Generate the caption now (no quotes, just the text):"""
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=150,
            )
        )
        
        caption = response.text.strip()
        # Clean up response
        caption = caption.strip('"').strip("'").split('\n')[0]
        
        if caption:
            logger.info(f"Generated artistic caption for {username} using Gemini")
            return caption
        else:
            return _generate_caption_fallback(username, total_commits, top_language)
            
    except Exception as e:
        logger.error(f"Gemini API error for artistic caption: {e}")
        raise


def _generate_caption_fallback(username: str, total_commits: int, top_language: str) -> str:
    """
    Fallback caption generation using templates
    """
    import random
    
    templates = [
        f"The digital odyssey of {username}: {total_commits} commits of {top_language} excellence",
        f"Crafting code in {top_language} - {username}'s {total_commits}-commit journey",
        f"{username}: Where {total_commits} commits meet {top_language} creativity",
        f"The coding journey of {username} is written in {top_language} and {total_commits} moments of brilliance",
        f"{username}'s {top_language} legacy: {total_commits} commits, infinite possibilities",
        f"Every line of {top_language} from {username} echoes through {total_commits} commits",
        f"In the world of {top_language}, {username} speaks fluently in {total_commits} commits",
        f"{username}'s {top_language} canvas: painted with {total_commits} brushstrokes of code",
        f"A {top_language} symphony by {username}, composed of {total_commits} perfect commits",
        f"{username} - {total_commits} commits, one {top_language} developer, infinite vision"
    ]
    
    caption = random.choice(templates)
    logger.info(f"Generated artistic caption for {username} using fallback templates")
    return caption


def analyze_vibe(commit_history: List[Dict]) -> str:
    """
    Analyze commit history to determine user's coding vibe.
    
    Detects if user is a 'Night Owl' (commits late) or 'Early Bird' (commits early).
    Returns theme preference: 'neon' for night owls, 'pastel' for early birds.
    
    Commit history format: List of dicts with 'date' (YYYY-MM-DD) and 'count' keys
    
    Args:
        commit_history: List of daily contribution records
        
    Returns:
        'neon' for night owl vibe, 'pastel' for early bird vibe
    """
    if not commit_history:
        logger.warning("Empty commit history for vibe analysis, defaulting to neon")
        return "neon"
    
    # Try ML analysis with Gemini if available
    if GEMINI_API_KEY and _HAS_GENAI and genai:
        try:
            return _analyze_vibe_with_gemini(commit_history)
        except Exception as e:
            logger.warning(f"Gemini API failed for vibe analysis: {e}, using heuristics")
    
    # Fallback to heuristic analysis
    return _analyze_vibe_heuristic(commit_history)


def _analyze_vibe_with_gemini(commit_history: List[Dict]) -> str:
    """
    Analyze vibe using Google Gemini API based on commit patterns
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare statistics from commit history
        from datetime import datetime
        
        total_commits = sum(c.get('count', 0) for c in commit_history)
        weekday_commits = 0
        weekend_commits = 0
        
        for entry in commit_history:
            try:
                date = datetime.strptime(entry.get('date', ''), '%Y-%m-%d')
                weekday = date.weekday()  # 0=Monday, 6=Sunday
                commits = entry.get('count', 0)
                
                if weekday < 5:  # Monday to Friday
                    weekday_commits += commits
                else:  # Saturday and Sunday
                    weekend_commits += commits
            except (ValueError, KeyError):
                continue
        
        high_activity_days = sum(1 for c in commit_history if c.get('count', 0) > 5)
        total_days = len(commit_history)
        
        prompt = f"""Analyze this developer's commit pattern and determine if they're a Night Owl or Early Bird.

Commit Statistics:
- Total Commits: {total_commits}
- Weekday Commits: {weekday_commits}
- Weekend Commits: {weekend_commits}
- High Activity Days (5+ commits): {high_activity_days} out of {total_days} days

Based on this pattern, is this developer more likely to be:
- A Night Owl (works late, prefers dark themes): Return "neon"
- An Early Bird (works early, prefers light themes): Return "pastel"

Analysis: Night Owls tend to have:
- More weekend commits (flexible schedule)
- Higher activity variance (erratic scheduling)
- Late-night commit patterns

Early Birds tend to have:
- Consistent weekday patterns (regular schedule)
- Lower variance (predictable schedule)
- Business hours commits

Return ONLY the word "neon" or "pastel" (no explanation):"""
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=20,
            )
        )
        
        vibe = response.text.strip().lower()
        
        # Validate response
        if vibe in ['neon', 'pastel']:
            logger.info(f"Vibe analysis with Gemini: {vibe}")
            return vibe
        else:
            logger.warning(f"Unexpected vibe response from Gemini: {vibe}, using heuristics")
            return _analyze_vibe_heuristic(commit_history)
            
    except Exception as e:
        logger.error(f"Gemini vibe analysis error: {e}")
        raise


def _analyze_vibe_heuristic(commit_history: List[Dict]) -> str:
    """
    Analyze vibe using heuristic pattern matching
    
    Detects night owl vs early bird based on:
    - Weekend vs weekday commit distribution
    - Consistency and variance of commits
    """
    if not commit_history:
        return "neon"  # Default to neon
    
    try:
        from datetime import datetime
        
        weekday_commits = 0
        weekend_commits = 0
        daily_activity = []
        
        for entry in commit_history:
            try:
                date = datetime.strptime(entry.get('date', ''), '%Y-%m-%d')
                weekday = date.weekday()  # 0=Monday, 6=Sunday
                commits = entry.get('count', 0)
                
                daily_activity.append(commits)
                
                if weekday < 5:  # Monday to Friday
                    weekday_commits += commits
                else:  # Saturday and Sunday
                    weekend_commits += commits
            except (ValueError, KeyError, TypeError):
                continue
        
        if not daily_activity:
            return "neon"
        
        # Calculate statistics
        total_commits = sum(daily_activity)
        avg_commits = total_commits / len(daily_activity) if daily_activity else 0
        
        # Standard deviation (measure of variance/erratic schedule)
        if len(daily_activity) > 1:
            variance = sum((x - avg_commits) ** 2 for x in daily_activity) / len(daily_activity)
            std_dev = variance ** 0.5
        else:
            std_dev = 0
        
        # Weekend/Weekday ratio
        weekend_ratio = weekend_commits / (total_commits + 0.001)  # Avoid division by zero
        
        # Activity consistency (number of zero-commit days)
        zero_days = sum(1 for x in daily_activity if x == 0)
        zero_ratio = zero_days / len(daily_activity) if daily_activity else 0
        
        # Night Owl indicators:
        # - High weekend activity (flexible schedule)
        # - High variance (erratic scheduling)
        # - More irregular pattern
        
        night_owl_score = 0
        
        # Weekend activity: night owls have > 30% weekend commits
        if weekend_ratio > 0.3:
            night_owl_score += 2
        
        # Variance: high variance suggests night owl (irregular sleeping)
        if std_dev > avg_commits * 1.5:  # High variance relative to mean
            night_owl_score += 2
        
        # More zero days means less consistent (night owl pattern)
        if zero_ratio > 0.3:
            night_owl_score += 1
        
        # Threshold: if score >= 3, likely night owl
        return "neon" if night_owl_score >= 3 else "pastel"
        
    except Exception as e:
        logger.error(f"Error in heuristic vibe analysis: {e}")
        return "neon"  # Default to neon on error
