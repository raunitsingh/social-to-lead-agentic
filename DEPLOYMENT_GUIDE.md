# Deployment Guide — Render

## Changes Made

 **webhook.py** — Converted to production-ready FastAPI
- Binds to `0.0.0.0:$PORT` (required for cloud platforms)
- Serves `index.html` at root `/`
- All chat/session endpoints consolidated
- CORS enabled for frontend requests

 **render.yaml** — Updated start command
```yaml
startCommand: uvicorn webhook:app --host 0.0.0.0 --port $PORT --workers 1
```
- `--workers 1`: Preserves session state (LangGraph thread_id)
- `--host 0.0.0.0`: Binds to all interfaces
- `--port $PORT`: Uses Render's dynamic PORT env var

 **requirements.txt** — Dependencies optimized
- Removed: Flask (replaced with FastAPI)
- Added: FastAPI, uvicorn[standard]
- Kept: LangChain, LangGraph, ChromaDB, etc. (no torch/nvidia)

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally on port 8080
uvicorn webhook:app --host 0.0.0.0 --port 8080

# Open browser
http://localhost:8080
```

## Expected Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Serve UI (index.html) |
| `/ui/*` | GET | Static assets in /ui folder |
| `/chat` | POST | Chat endpoint (LangGraph agent) |
| `/session/{id}` | DELETE | Reset session memory |
| `/health` | GET | Health check |

## Deployment to Render

1. Push to Git:
   ```bash
   git add webhook.py render.yaml requirements.txt
   git commit -m "Fix deployment: FastAPI + proper PORT binding"
   git push
   ```

2. **If using render.yaml** (Render Dashboard → GitHub → select this repo):
   - Render auto-detects `render.yaml`
   - Deploys with correct start command

3. **If using Web Service UI**:
   - Runtime: Python
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn webhook:app --host 0.0.0.0 --port $PORT --workers 1`
   - Add Env Vars: `GROQ_API_KEY`, `LLM_MODEL`, `PYTHONPATH=.`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No open ports detected" | Ensure `--host 0.0.0.0` in start command |
| UI not loading | Check `/health` returns `{"status":"ok"}` |
| Static files 404 | Verify `ui/` folder exists with `index.html` |
| "Address already in use" | `--workers 1` prevents multi-process conflicts |

## Notes

- **Session State**: Runs with `--workers 1` to maintain thread_id in-memory
- **Production Grade**: Use Gunicorn for horizontal scaling (requires refactoring)
- **UI Folder**: Must exist at runtime (included in git)
