# tests/conftest.py
import pytest


@pytest.fixture
def mock_user_data():
    """Shared mock GitHub user data for all generator tests."""
    return {
        "username":      "testuser",
        "name":          "Test User",
        "total_stars":   120,
        "total_commits": 450,
        "public_repos":  25,
        "followers":     85,
        "following":     40,
        "top_languages": {"Python": 60, "JavaScript": 30, "CSS": 10},
        "top_repos": [
            {
                "name":        "awesome-project",
                "description": "A really cool project",
                "language":    "Python",
                "stars":       42,
                "forks":       10,
                "updated_at":  "2024-01-01"
            },
            {
                "name":        "web-app",
                "description": "A web application",
                "language":    "JavaScript",
                "stars":       18,
                "forks":       5,
                "updated_at":  "2024-02-01"
            },
        ],
        "contributions": [1, 3, 0, 5, 2, 8, 4],
        "streak":        7,
        "longest_streak": 21,
    }


@pytest.fixture
def show_options_all():
    """All stats visible."""
    return {
        "stars":     True,
        "commits":   True,
        "repos":     True,
        "followers": True
    }


@pytest.fixture
def show_options_none():
    """All stats hidden."""
    return {
        "stars":     False,
        "commits":   False,
        "repos":     False,
        "followers": False
    }