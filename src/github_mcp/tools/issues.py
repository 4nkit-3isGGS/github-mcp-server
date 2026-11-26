from typing import Literal
from mcp.server import MCPServer
from github_mcp.client.github import github_client, GitHubAPIError

def registry_issue_tools(mcp: MCPServer) -> None:
    """Register Github issue managemnet tools."""

    @mcp.tool()
    async def list_issues(
        owner: str,
        repo: str,
        state: Literal["open", "closed", "all"] = "open",
        per_page: int = 10
    ) -> dict:
        """List issues in a GitHub repository (excludes pull requests)."""
        try:
            limit = max(1, min(per_page, 30))
            data = await github_client.get(
                f"/repos/{owner}/{repo}/issues",
                params={"state": state, "per_page": limit},
            )
            issues = [
                {
                    "number": item.get("number"),
                    "title": item.get("title"),
                    "state": item.get("state"),
                    "author": item.get("user", {}).get("login"),
                    "labels": [lbl.get("name") for lbl in item.get("labels", [])],
                    "created_at": item.get("created_at"),
                    "html_url": item.get("html_url"),
                }
                for item in data
                if "pull_request" not in item
            ]
            return {"count": len(issues), "issues": issues}
        except GitHubAPIError as exc:
            return {"error": str(exc)}

    @mcp.tool()
    async def create_issue(
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: list[str] | None = None,
    ) -> dict:
        """Create new issue for a Github repository."""
        try:
            payload: dict = {"title": title, "body": body}
            if labels:
                payload["labels"] = labels
            data = await github_client.post(
                f"/repos/{owner}/{repo}/issues",
                json=payload,
            )
            return {
                "number": data.get("number"),
                "title": data.get("title"),
                "state": data.get("state"),
                "html_url": data.get("html_url"),
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}
    
    @mcp.tool()
    async def add_issue_comment(
        owner: str,
        repo: str,
        issue_number: int,
        body: str,
    ) -> dict:
        """Add a comment to an existing GitHub issue or pull request."""
        try:
            data = await github_client.post(
                f"/repos/{owner}/{repo}/issues/{issue_number}/comments",
                json={"body": body},
            )
            return {
                "id": data.get("id"),
                "author": data.get("user", {}).get("login"),
                "html_url": data.get("html_url"),
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}