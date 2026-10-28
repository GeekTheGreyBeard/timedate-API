# Timedate API & MCP Server

A small API that returns the current date and time for an IANA timezone, and an MCP (Model Context Protocol) server that exposes the same endpoints.

## What it does

`POST /api/timedate` takes a timezone name and returns the current local time, that same moment in UTC, a Unix timestamp, the UTC offset, and the timezone abbreviation. Names come from Python's `zoneinfo` database (the `tzdata` package).

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/timedate` | Current time for a timezone |
| `GET` | `/api/timezones` | Supported IANA names |
| `GET` | `/api/usage` | Endpoint list with examples |
| `GET` | `/health` | Status and how many timezones are loaded |
| `GET` | `/docs` | OpenAPI docs |

`GET /api/timezones` accepts two optional filters: `region` (a prefix such as `America`, `Europe`, or `Asia`) and `query` (a case-insensitive substring). An unknown timezone returns HTTP 400, with `error` set to `Invalid Timezone` and a message that points at `GET /api/timezones`.

An MCP server is mounted at `/mcp` and exposes these endpoints as tools. The app listens on port **8200**.

## Requirements

- Docker with Docker Compose, or Python 3.11
- Port 8200 free on the host

## Setup

With Docker, from the project root:

```sh
sudo docker compose up -d --build
```

Compose publishes port 8200 and checks `GET /health`.

Without Docker:

```sh
pip install -r requirements.txt
python timedate_app.py
```

## Usage

```sh
curl -X POST http://localhost:8200/api/timedate \
  -H "Content-Type: application/json" \
  -d '{"timezone": "Europe/London"}'
```

Example response (the clock values change; the fields do not):

```json
{
  "datetime": "2026-05-15T19:50:03.173125+01:00",
  "timezone": "Europe/London",
  "utc_datetime": "2026-05-15T18:50:03.173125+00:00",
  "unix_timestamp": 1789411803,
  "utc_offset": "+01:00",
  "abbreviation": "BST"
}
```

```sh
curl http://localhost:8200/health
curl http://localhost:8200/api/usage
curl "http://localhost:8200/api/timezones?region=America&query=denver"
```

## Tests

```sh
pip install -r requirements-dev.txt
pytest test_timedate_app.py
```
