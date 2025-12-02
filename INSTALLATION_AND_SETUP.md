# Lazy MCP Installation & Setup Guide

## Overview
Lazy MCP is a hierarchical MCP proxy that provides access to **145 tools across 9 servers** through an efficient lazy-loading meta-tool system. This eliminates token overhead by loading tool definitions only when needed.

## Quick Start

### Prerequisites
- Windows 10+ with PowerShell
- Node.js 18+ (for npx commands)
- Git (for version control)
- Docker (optional, only if using github-docker server)

### Installation Steps

1. **Clone or navigate to lazy-mcp directory**
   ```powershell
   cd c:\All-Beta-Builds\lazy-mcp
   ```

2. **Build the mcp-proxy binary**
   ```powershell
   go build -o .\build\mcp-proxy.exe .\cmd\mcp-proxy
   ```

3. **Add to Claude Desktop config**
   
   Edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "lazy-mcp": {
         "command": "c:\\All-Beta-Builds\\lazy-mcp\\build\\mcp-proxy.exe",
         "args": [
           "--config",
           "c:\\All-Beta-Builds\\lazy-mcp\\config.json"
         ],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN",
           "FIRECRAWL_API_KEY": "fc_YOUR_KEY",
           "TAVILY_API_KEY": "tvly_YOUR_KEY"
         },
         "disabled": false
       }
     }
   }
   ```

4. **Set environment variables** (or add to `.env` file)
   ```powershell
   $env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_YOUR_TOKEN"
   $env:FIRECRAWL_API_KEY = "fc_YOUR_KEY"
   $env:TAVILY_API_KEY = "tvly_YOUR_KEY"
   ```

5. **Restart Claude Desktop**
   - Close completely
   - Reopen to load lazy-mcp

## Configuration

### config.json Structure
```json
{
  "mcpProxy": {
    "name": "MCP Lazy Load Proxy",
    "version": "5.2.0",
    "type": "stdio",
    "hierarchyPath": "c:\\All-Beta-Builds\\lazy-mcp\\testdata\\mcp_hierarchy",
    "options": {
      "lazyLoad": true
    }
  },
  "mcpServers": {
    "server-name": {
      "transportType": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@namespace/package"],
      "env": {},
      "options": {
        "lazyLoad": true
      }
    }
  }
}
```

### Available Servers (9 total, 145 tools)
- **desktop-commander** (25 tools) - File operations, process management, terminal control
- **filesystem** (14 tools) - File reading/writing, directory operations, search
- **github** (26 tools) - Repository management, issues, pull requests, code search
- **github-docker** (40 tools) - Enhanced GitHub with team management & advanced reviews
- **firecrawl** (6 tools) - Web scraping, content extraction, site mapping
- **playwright** (22 tools) - Browser automation, web testing, page interaction
- **puppeteer** (7 tools) - Lightweight browser control, screenshots, DOM manipulation
- **tavily** (4 tools) - Web search, content extraction, knowledge retrieval
- **sequential-thinking** (1 tool) - Structured reasoning, problem decomposition

## Regenerating the Hierarchy

If you modify `config.json`, regenerate the tool hierarchy:

```powershell
# Build the structure generator
go build -o .\build\structure_generator.exe .\structure_generator\cmd

# Generate new hierarchy from config
.\build\structure_generator.exe -config .\config.json

# Replace old hierarchy with new one
Remove-Item -Recurse -Force .\testdata\mcp_hierarchy
Copy-Item -Recurse .\structure .\testdata\mcp_hierarchy
```

## Verifying Installation

1. **Check tool availability** (in Claude Desktop or your application):
   ```
   User: "Check your tools"
   Agent: [Queries lazy-mcp and returns 145 tools across 9 servers]
   ```

2. **Test a tool**:
   ```
   User: "List files in C:\zai-beta with depth 1"
   Agent: [Uses desktop-commander.list_directory]
   ```

3. **Check logs**:
   - Claude Desktop logs appear in terminal/console
   - Look for "sse server listening" or "Loaded 145 hierarchy nodes"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "mcp-proxy not found" | Run `go build -o .\build\mcp-proxy.exe .\cmd\mcp-proxy` |
| "hierarchy not found" | Run structure generator and verify testdata/mcp_hierarchy exists |
| "tool failing silently" | Check API keys in env vars (GITHUB_TOKEN, FIRECRAWL_API_KEY, etc.) |
| "slow tool loading" | Normal on first call - hierarchy is cached after initial load |
| "Docker server won't run" | Ensure Docker Desktop is running if using github-docker |

## Performance Notes

- **First tool query**: ~2-3 seconds (hierarchy loads into memory)
- **Subsequent queries**: <100ms (cached)
- **Token savings**: ~60-70% vs loading individual servers
- **Hierarchy size**: 145 tools = ~50KB in memory (negligible overhead)

## Next Steps

See the **SYSTEM_PROMPT.md** file for agent instructions on how to use Lazy MCP effectively.
