from mcp.server import MCPServer

from github_mcp.client.github import github_client, GitHubAPIError

mcp = MCPServer("Github MCP Server")

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

def main() -> None:
    mcp.run()

if __name__ == "__main__":
    main()