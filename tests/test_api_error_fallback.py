from fastapi.testclient import TestClient

from api.main import app
from utils import github_api


def test_stats_returns_user_not_found_svg(monkeypatch):
    def raise_not_found(*_args, **_kwargs):
        raise github_api.UserNotFoundError("missing-user")

    monkeypatch.setattr(github_api, "get_live_github_data", raise_not_found)

    with TestClient(app) as client:
        response = client.get("/api/stats", params={"username": "missing-user"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert "User Not Found" in response.text


def test_languages_returns_rate_limited_svg(monkeypatch):
    def raise_rate_limited(*_args, **_kwargs):
        raise github_api.RateLimitExceededError("GitHub API rate limit exceeded")

    monkeypatch.setattr(github_api, "get_live_github_data", raise_rate_limited)

    with TestClient(app) as client:
        response = client.get("/api/languages", params={"username": "octocat"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert "Rate Limited" in response.text


def test_repos_returns_api_error_svg(monkeypatch):
    def raise_api_error(*_args, **_kwargs):
        raise github_api.GitHubApiError("Service unavailable")

    monkeypatch.setattr(github_api, "get_live_github_data", raise_api_error)

    with TestClient(app) as client:
        response = client.get("/api/repos", params={"username": "octocat"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert "GitHub API Error" in response.text
    assert "Service unavailable" in response.text
