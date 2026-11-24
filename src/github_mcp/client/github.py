from typing import Any

import httpx

from github_mcp.config import settings


class GitHubAPIError(Exception):
    """Raised when GitHub returns an error response."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"GitHub API error {status_code}: {message}")


class GitHubClient:
    """Thin async wrapper around the GitHub REST API."""

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.github_api_base,
            timeout=settings.request_timeout,
            headers={
                "Authorization": f"Bearer {settings.github_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Single place where every HTTP call happens."""
        response = await self._client.request(method, path, **kwargs)

        if response.is_error:
            try:
                message = response.json().get("message", response.text)
            except ValueError:
                message = response.text
            raise GitHubAPIError(response.status_code, message)

        if response.status_code == 204:  # No Content
            return None
        return response.json()

    # ---- Convenience helpers ----
    async def get(self, path: str, params: dict | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: dict | None = None) -> Any:
        return await self._request("POST", path, json=json)

    async def patch(self, path: str, json: dict | None = None) -> Any:
        return await self._request("PATCH", path, json=json)

    async def close(self) -> None:
        await self._client.aclose()


github_client = GitHubClient()