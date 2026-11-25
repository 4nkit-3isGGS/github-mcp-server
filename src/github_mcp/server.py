from mcp.server import MCPServer

from github_mcp.tools.repositories import register_repository_tools

mcp = MCPServer("Github MCP Server")

register_repository_tools(mcp)

def main() -> None:
    mcp.run()

if __name__ == "__main__":
    main()