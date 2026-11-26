from typing import Literal
from mcp.server import MCPServer
from github_mcp.client.github import GitHubAPIError, github_client

def register_pull_request_tools(mcp: MCPServer) -> None:
    """Register GitHub Pull Request management tools."""

    @mcp.tool()
    async def list_pull_requests(
        owner: str,
        repo: str,
        state: Literal["open", "closed", "all"] = "open",
        per_page: int = 10,
    ) -> dict:
        """List pull requests in a GitHub repository."""
        try:
            limit = max(1, min(per_page, 30))
            data = await github_client.get(
                f"/repos/{owner}/{repo}/pulls",
                params={"state": state, "per_page": limit},
            )
            pulls = [
                {
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "state": pr.get("state"),
                    "draft": pr.get("draft"),
                    "author": pr.get("user", {}).get("login"),
                    "head": pr.get("head", {}).get("ref"),
                    "base": pr.get("base", {}).get("ref"),
                    "created_at": pr.get("created_at"),
                    "html_url": pr.get("html_url"),
                }
                for pr in data
            ]
            return {"count": len(pulls), "pull_requests": pulls}
        except GitHubAPIError as exc:
            return {"error": str(exc)}

        
    @mcp.tool()
    async def get_pull_request(
        owner: str,
        repo: str,
        pull_number: int,
    ) -> dict:
        """Get detailed information about a specific pull request."""
        try:
            pr = await github_client.get(
                f"/repos/{owner}/{repo}/pulls/{pull_number}"
            )
            return {
                "number": pr.get("number"),
                "title": pr.get("title"),
                "body": pr.get("body"),
                "state": pr.get("state"),
                "merged": pr.get("merged"),
                "mergeable": pr.get("mergeable"),
                "author": pr.get("user", {}).get("login"),
                "head": pr.get("head", {}).get("ref"),
                "base": pr.get("base", {}).get("ref"),
                "commits": pr.get("commits"),
                "additions": pr.get("additions"),
                "deletions": pr.get("deletions"),
                "changed_files": pr.get("changed_files"),
                "html_url": pr.get("html_url"),
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}

    @mcp.tool()
    async def list_pull_request_files(
        owner: str,
        repo: str,
        pull_number: int,
        per_page: int = 15,
    ) -> dict:
        """List changed files and their diff patches for a pull request."""
        try:
            limit = max(1, min(per_page, 30))
            data = await github_client.get(
                f"/repos/{owner}/{repo}/pulls/{pull_number}/files",
                params={"per_page": limit},
            )
            files = [
                {
                    "filename": f.get("filename"),
                    "status": f.get("status"),
                    "additions": f.get("additions"),
                    "deletions": f.get("deletions"),
                    "patch": f.get("patch"),
                }
                for f in data
            ]
            return {"count": len(files), "files": files}
        except GitHubAPIError as exc:
            return {"error": str(exc)}

        
    @mcp.tool()
    async def create_pull_request(
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str = "main",
        body: str = "",
        draft: bool = False,
    ) -> dict:
        """Create a new pull request from `head` branch into `base` branch."""
        try:
            data = await github_client.post(
                f"/repos/{owner}/{repo}/pulls",
                json={
                    "title": title,
                    "head": head,
                    "base": base,
                    "body": body,
                    "draft": draft,
                },
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
    async def create_pull_request_review(
        owner: str,
        repo: str,
        pull_number: int,
        body: str,
        event: Literal["COMMENT", "APPROVE", "REQUEST_CHANGES"] = "COMMENT",
    ) -> dict:
        """Submit a review (COMMENT, APPROVE, or REQUEST_CHANGES) on a pull request."""
        try:
            data = await github_client.post(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews",
            json={"body": body, "event": event},
        )
            return {
            "id": data.get("id"),
            "state": data.get("state"),
            "author": data.get("user", {}).get("login"),
            "html_url": data.get("html_url"),
        }
        except GitHubAPIError as exc:
            return {"error": str(exc)}