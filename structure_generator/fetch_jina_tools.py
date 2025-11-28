import asyncio
import json
import os
import httpx
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.types import ClientCapabilities, InitializeRequest, Implementation

async def fetch_jina_tools():
    api_key = os.environ.get("JINA_API_KEY")
    if not api_key:
        print("Error: JINA_API_KEY not set")
        return

    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://mcp.jina.ai/sse"

    print(f"Connecting to {url}...")
    
    # We need to use the MCP SDK to handle the SSE connection and protocol
    # But installing mcp might be needed.
    # Let's try a raw implementation if SDK is not available or complex.
    
    # Actually, let's try to use the mcp-proxy I just installed? 
    # No, that's for serving.
    
    # Let's try to use the mcp python package.
    try:
        async with sse_client(url, headers=headers) as (read, write):
            print("Connected!")
            
            # Initialize
            init_result = await write.initialize(
                InitializeRequest(
                    protocolVersion="2024-11-05",
                    capabilities=ClientCapabilities(),
                    clientInfo=Implementation(name="fetcher", version="1.0")
                )
            )
            print("Initialized!")
            
            # List tools
            tools_result = await write.list_tools()
            
            tools_data = {
                "serverName": "jina",
                "tools": [tool.model_dump() for tool in tools_result.tools]
            }
            
            with open("jina_tools.json", "w") as f:
                json.dump(tools_data, f, indent=2)
                
            print(f"Saved {len(tools_result.tools)} tools to jina_tools.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(fetch_jina_tools())
