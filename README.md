# Timedate API & MCP Server

This project provides a FastAPI application with an MCP (Model Context Protocol) server. It returns the current time and date for a submitted timezone.

## Features
- **API endpoint:** `/api/timedate` (POST)
- **Usage endpoint:** `/api/usage` (GET)
- **Timezone discovery:** `/api/timezones` (GET)
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

### 3. Discover Usage
```sh
curl http://localhost:8200/api/usage
```

### 4. List Supported Timezones
```sh
curl http://localhost:8200/api/timezones
```

### 5. Run Tests
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

## API Endpoints

- `GET /api/usage` returns endpoint descriptions and example requests/responses.
- `GET /api/timezones` returns the supported IANA timezone names.
- `POST /api/timedate` accepts `{"timezone": "Europe/London"}` and returns the current ISO-8601 date/time for that timezone.

## Files
- `timedate_app.py` — Main FastAPI app
- `test_timedate_app.py` — Tests for the API
- `Dockerfile` — Container build
- `docker-compose.yml` — Orchestration and healthcheck
- `requirements.txt` — Python dependencies
- `requirements-dev.txt` — Test dependencies
