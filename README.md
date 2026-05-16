# Timedate API & MCP Server

This project provides a FastAPI application with an MCP (Model Context Protocol) server. It returns the current time and date for a submitted timezone.

## Features
- **API endpoint:** `/api/timedate` (POST)
- **Health endpoint:** `/health` (GET)
- **Usage endpoint:** `/api/usage` (GET)
- **Timezone discovery:** `/api/timezones` (GET, with optional `region` and `query` filters)
- **Extended time metadata:** local datetime, UTC datetime, Unix timestamp, UTC offset, and timezone abbreviation
- **OpenAPI docs:** request/response schemas and examples at `/docs`
- **MCP server:** `/mcp` (exposes all API endpoints)
- **Docker & Docker Compose** support
- **Healthcheck** for production readiness
- **Pinned dependencies** for reproducible installs/builds

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

### 3. Check Health
```sh
curl http://localhost:8200/health
```

### 4. Discover Usage
```sh
curl http://localhost:8200/api/usage
```

### 5. List Supported Timezones
```sh
curl http://localhost:8200/api/timezones
```

### 6. Filter Timezones
```sh
curl "http://localhost:8200/api/timezones?region=America&query=denver"
```

### 7. Run Tests
```sh
pip install -r requirements-dev.txt
pytest test_timedate_app.py
```

## Example Response

```json
{
  "datetime": "2026-05-15T19:50:03.173125-06:00",
  "timezone": "America/Denver",
  "utc_datetime": "2026-05-16T01:50:03.173125+00:00",
  "unix_timestamp": 1789437003,
  "utc_offset": "-06:00",
  "abbreviation": "MDT"
}
```

## API Endpoints

- `GET /health` returns service health and timezone catalog count.
- `GET /api/usage` returns endpoint descriptions and example requests/responses.
- `GET /api/timezones` returns the supported IANA timezone names. Optional query params:
  - `region`: filters by timezone region prefix, such as `America`, `Europe`, or `Asia`.
  - `query`: filters by case-insensitive substring.
- `POST /api/timedate` accepts `{"timezone": "Europe/London"}` and returns current time metadata for that timezone.

Invalid timezone responses use a structured error body:

```json
{
  "error": "Invalid Timezone",
  "message": "Use GET /api/timezones to discover supported IANA timezone names."
}
```

## Files
- `timedate_app.py` — Main FastAPI app
- `test_timedate_app.py` — Tests for the API
- `Dockerfile` — Container build
- `docker-compose.yml` — Orchestration and healthcheck
- `requirements.txt` — Python dependencies
- `requirements-dev.txt` — Test dependencies
