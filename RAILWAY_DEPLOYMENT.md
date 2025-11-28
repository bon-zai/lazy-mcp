# Railway Deployment Guide

## Overview
lazy-mcp is a hierarchical MCP proxy that aggregates 133 tools from 9 MCP servers. This guide walks through deploying to Railway with full environment control.

## Prerequisites
- Railway account: https://railway.app
- Docker support in Railway (included in all plans)
- Git repository connected to Railway

## Environment Variables

Set these in Railway project settings:

```
PORT=8080
BRAVE_API_KEY=your_brave_api_key
MEM0_API_KEY=your_mem0_api_key
GITHUB_TOKEN=your_github_token
JINA_API_KEY=your_jina_api_key
TAVILY_API_KEY=your_tavily_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
```

**Note:** Environment variables in Railway override config.json placeholders like `${PORT}` and `${TAVILY_API_KEY}`.

## Building & Deployment

### Option 1: Railway CLI (Recommended for Control)

```bash
# 1. Build locally
go build -o build/mcp-proxy.exe ./cmd/mcp-proxy

# 2. Push to Railway
railway login
railway link  # Select or create project
railway up
```

### Option 2: GitHub Integration

1. Push code to GitHub
2. In Railway dashboard: Add service → GitHub repo
3. Select this repository
4. Railway auto-builds from Dockerfile

## Dockerfile Verification

The included `Dockerfile`:
- Builds Go binary: `mcp-proxy`
- Installs Node.js for MCP servers
- Exposes HTTP on `$PORT` (default 8080)
- Loads tool hierarchy from `testdata/mcp_hierarchy/`

## MCP Servers

All 9 servers are lazily loaded:

1. **filesystem** - File operations (14 tools)
2. **firecrawl** - Web search & crawl (6 tools)
3. **github** - Repository operations (26 tools)
4. **github-docker** - GitHub via Docker (40 tools)
5. **mem0** - Memory management (2 tools)
6. **playwright** - Browser automation (22 tools)
7. **puppeteer** - Puppeteer browser (7 tools)
8. **sequential-thinking** - Reasoning (1 tool)
9. **tavily** - Web search (4 tools)

## Endpoint

Once deployed, access via:

```
http://<railway-app-url>/sse
http://<railway-app-url>/message  (POST)
```

## Connection in Claude/Zai

Configure MCP client to use:
```
sse
http://<railway-url>/sse
```

## Development Locally

### Setup
```bash
# 1. Create .env.local from template
cp .env.example .env.local
# Edit with your API keys

# 2. Build
go build -o build/mcp-proxy.exe ./cmd/mcp-proxy

# 3. Run in SSE mode
./build/mcp-proxy.exe
# Server listens on http://localhost:8080/sse
```

### Testing Tools

```bash
# List all available tools
curl http://localhost:8080/sse

# Execute a tool
curl -X POST http://localhost:8080/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"filesystem.read_file","arguments":{"path":"/path/to/file"}}}'
```

## Notes

- All API keys are environment-driven. No hardcoded secrets.
- `.env` and `.env.local` are ignored by git.
- Tool hierarchy is pre-generated in `testdata/mcp_hierarchy/` for fast lazy-loading.
- Each MCP server runs as a separate stdio process, managed by lazy-mcp proxy.

## Troubleshooting

### Port already in use
```bash
lsof -i :8080  # macOS/Linux
Get-NetTCPConnection -LocalPort 8080  # Windows
```

### Missing tools
Check that hierarchy files exist:
```bash
ls testdata/mcp_hierarchy/firecrawl/
```

### Environment variables not loading
Verify in Railway dashboard under "Variables" section. Restart deployment after changes.

## Git Management

```bash
# Stage Railway-ready changes
git add config.json .gitignore

# View what's being committed
git status

# Push to trigger Railway build
git push origin main
```

---

**Last Updated:** 2025-11-28
