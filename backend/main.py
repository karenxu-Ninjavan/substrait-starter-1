"""
Weekly P&L — single-file FastAPI app.

Substrait requires three things of this file:
  1. the server listens on port 8000          (set in cicd/Dockerfile.backend)
  2. GET /health returns 200                  (Substrait's readiness check)
  3. the JSON API lives under /api            (Substrait routes /api here)

The full weekly P&L dashboard lives in `page.html` (sibling file); this module
reads and serves it. Regenerate `page.html` locally from the upstream Excel
data, then redeploy — no Python changes needed for content refreshes.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

APP_NAME = "Weekly P&L"

app = FastAPI(title=APP_NAME, docs_url="/api/docs")

PAGE_PATH = Path(__file__).parent / "page.html"


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.get("/api/info")
def info():
    return {
        "app": APP_NAME,
        "week": PAGE_PATH.read_text(encoding="utf-8")
            .split('id="weekSub">')[1].split('<')[0]
            if 'id="weekSub">' in PAGE_PATH.read_text(encoding="utf-8")
            else None,
    }


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def homepage():
    return HTMLResponse(content=PAGE_PATH.read_text(encoding="utf-8"))
