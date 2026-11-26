from mcp.server import MCPServer

from github_mcp.tools.repositories import register_repository_tools
from github_mcp.tools.issues import registry_issue_tools
from github_mcp.tools.pull_requests import register_pull_request_tools

mcp = MCPServer("Github MCP Server")

register_repository_tools(mcp)
registry_issue_tools(mcp)
register_pull_request_tools(mcp)

def main() -> None:
    mcp.run()

if __name__ == "__main__":
    main()