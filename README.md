# Timedate API & MCP Server

This project provides a FastAPI application with an MCP (Model Context Protocol) server. It returns the current time and date for a submitted timezone.

## Features
- **API endpoint:** `/api/timedate` (POST)
- **MCP server:** `/mcp` (exposes all API endpoints)
- **Docker & Docker Compose** support
- **Healthcheck** for production readiness

## Usage

### 1. Build and Run with Docker Compose
```sh
# From the project root
sudo docker compose up -d --build
```

### 2. Test the API
```sh
curl -X POST http://localhost:8200/api/timedate \
  -H "Content-Type: application/json" \
  -d '{"timezone": "Europe/London"}'
```

### 3. Run Tests
```sh
pip install -r requirements-dev.txt
pytest test_timedate_app.py
```

## Example Response

```json
{
  "datetime": "2026-05-15T19:50:03.173125-06:00",
  "timezone": "America/Denver"
}
```

## Files
- `timedate_app.py` — Main FastAPI app
- `test_timedate_app.py` — Tests for the API
- `Dockerfile` — Container build
- `docker-compose.yml` — Orchestration and healthcheck
- `requirements.txt` — Python dependencies
- `requirements-dev.txt` — Test dependencies
