from mcp.server import MCPServer

from github_mcp.client.github import github_client, GitHubAPIError

def register_repository_tools(mcp: MCPServer) -> None:
    """Register repository and user-related GitHub tools."""
    @mcp.tool()
    async def get_authenticated_user() -> dict:
        """Get details about the currently authenticated GitHub user."""
        try:
            data = await github_client.get("/user")
            return {
                "login": data.get("login"),
                "name": data.get("name"),
                "public_repos": data.get("public_repos"),
                "html_url": data.get("html_url"),
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}

    @mcp.tool()
    async def get_repository(owner: str, repo: str) -> dict:
        """Get metadata for a specific GitHub repository (stars, forks, default branch, description)."""
        try:
            data = await github_client.get(f"/repos/{owner}/{repo}")
            return {
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "default_branch": data.get("default_branch"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "open_issues": data.get("open_issues_count"),
                "language": data.get("language"),
                "html_url": data.get("html_url"),
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}
            
    @mcp.tool()
    async def search_repositories(query: str, per_page: int = 5) -> dict:
        """Search GitHub repositories by query string (e.g. 'fastmcp language:python')."""
        try:
            limit = max(1, min(per_page, 20))
            data = await github_client.get(
                "/search/repositories",
                params={"q": query, "per_page": limit},
            )
            items = [
                {
                    "full_name": item.get("full_name"),
                    "description": item.get("description"),
                    "stars": item.get("stargazers_count"),
                    "language": item.get("language"),
                    "html_url": item.get("html_url"),
                }
                for item in data.get("items", [])
            ]
            return {
                "total_count": data.get("total_count", 0),
                "results": items,
            }
        except GitHubAPIError as exc:
            return {"error": str(exc)}