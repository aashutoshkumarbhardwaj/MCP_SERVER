from fastmcp import FastMCP
from main import app

mcp = FastMCP.from_fastapi(
    app=app,
    name="expense tracker server"
)

if __name__ == "__main__":
    # Hugging Face provides its web services on port 7860
    # FastMCP auto-creates the /sse and /messages endpoints for you
    mcp.run(transport="sse", host="0.0.0.0", port=7860)
