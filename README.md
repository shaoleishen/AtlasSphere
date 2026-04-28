
## The Data Plane Concept
AtlasSphere addresses the Memory OOM (Out of Memory) issue prevalent in agentic tools handing 30GB+ `.h5ad` single-cell datasets. The internal memory reference mechanism dictates that MCP JSON messages exclusively transport lightweight pointers (`UUID-x` identifiers), guaranteeing that core data processing and ML algorithm routing happens purely within the isolated local context!

## Setup and Quick Action

### 1. Local Dev Installation
```bash
# Strongly recommended: use `uv` package manager
uv pip install -e .
# To install heavily-weighted analytics dependencies like scanpy:
uv pip install -e ".[omics]"
```

### 2. Connect with Claude Code / Claw CLI
To enable seamless structural bio-agents right from your terminal without custom code logic:
Inject this MCP into your claw configuration:
```json
"mcpServers": {
    "AtlasSphere_Omics": {
        "command": "atlas-mcp",
        "args": []
    }
}
```

### 3. Deploy via Docker
Included is a highly-optimized Dockerfile allowing rapid orchestration:
```bash
docker build -t atlassphere-hub:latest .
docker run -p 8000:8000 atlassphere-hub:latest
```
