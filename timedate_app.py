from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

from fastapi import Body, FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi_mcp import FastApiMCP

TIMEZONES = sorted(available_timezones())

app = FastAPI(
    title="Timedate API & MCP Server",
    description="Returns current date/time metadata for IANA timezones.",
    version="1.1.0",
)

class TimeDateRequest(BaseModel):
    timezone: str = Field(
        ...,
        examples=["Europe/London"],
        description="IANA timezone name. Use GET /api/timezones to discover supported values.",
    )

class TimeDateResponse(BaseModel):
    datetime: str
    timezone: str
    utc_datetime: str
    unix_timestamp: int
    utc_offset: str
    abbreviation: str | None

class UsageExample(BaseModel):
    method: str
    path: str
    description: str
    example_request: dict | None = None
    example_response: dict

class UsageResponse(BaseModel):
    service: str
    description: str
    endpoints: list[UsageExample]

class TimezonesResponse(BaseModel):
    count: int
    timezones: list[str]

class HealthResponse(BaseModel):
    status: str
    service: str
    timezone_count: int

class ErrorResponse(BaseModel):
    error: str
    message: str

def format_utc_offset(dt: datetime) -> str:
    offset = dt.utcoffset()
    if offset is None:
        return "+00:00"
    total_seconds = int(offset.total_seconds())
    sign = "+" if total_seconds >= 0 else "-"
    total_seconds = abs(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{sign}{hours:02d}:{minutes:02d}"

@app.get("/health", response_model=HealthResponse, tags=["system"], operation_id="get_health")
async def get_health():
    return {
        "status": "ok",
        "service": "Timedate API",
        "timezone_count": len(TIMEZONES),
    }

@app.get("/api/usage", response_model=UsageResponse, tags=["timedate"], operation_id="get_usage")
async def get_usage():
    return {
        "service": "Timedate API",
        "description": "Returns the current date and time for a submitted IANA timezone.",
        "endpoints": [
            {
                "method": "POST",
                "path": "/api/timedate",
                "description": "Get the current date and time for a timezone.",
                "example_request": {"timezone": "Europe/London"},
                "example_response": {
                    "datetime": "2026-05-15T19:50:03.173125+01:00",
                    "timezone": "Europe/London",
                    "utc_datetime": "2026-05-15T18:50:03.173125+00:00",
                    "unix_timestamp": 1789411803,
                    "utc_offset": "+01:00",
                    "abbreviation": "BST",
                },
            },
            {
                "method": "GET",
                "path": "/api/timezones",
                "description": "List supported IANA timezone names.",
                "example_request": None,
                "example_response": {
                    "count": 1,
                    "timezones": ["America/Denver"],
                },
            },
        ],
    }

@app.get("/api/timezones", response_model=TimezonesResponse, tags=["timedate"], operation_id="list_timezones")
async def list_timezones(
    query: str | None = Query(default=None, description="Case-insensitive substring filter."),
    region: str | None = Query(default=None, description="Timezone region prefix, such as America, Europe, or Asia."),
):
    timezones = TIMEZONES
    if region:
        region_prefix = f"{region.strip().rstrip('/')}/".lower()
        timezones = [tz for tz in timezones if tz.lower().startswith(region_prefix)]
    if query:
        normalized_query = query.strip().lower()
        timezones = [tz for tz in timezones if normalized_query in tz.lower()]
    return {"count": len(timezones), "timezones": timezones}

@app.post(
    "/api/timedate",
    response_model=TimeDateResponse,
    responses={400: {"model": ErrorResponse, "description": "Invalid timezone"}},
    tags=["timedate"],
    operation_id="get_time_date",
)
async def get_time_date(
    request: TimeDateRequest = Body(
        ...,
        examples=[{"timezone": "Europe/London"}],
    )
):
    tz_name = request.timezone
    try:
        tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Invalid Timezone",
                "message": "Use GET /api/timezones to discover supported IANA timezone names.",
            },
        )
    now = datetime.now(tz)
    utc_now = now.astimezone(UTC)
    return {
        "datetime": now.isoformat(),
        "timezone": tz_name,
        "utc_datetime": utc_now.isoformat(),
        "unix_timestamp": int(now.timestamp()),
        "utc_offset": format_utc_offset(now),
        "abbreviation": now.tzname(),
    }

# Expose all endpoints via MCP at /mcp
mcp = FastApiMCP(
    app,
    name="Timedate MCP Server",
    description="Provides time and date for a given timezone.",
    describe_all_responses=True,
    describe_full_response_schema=True
)
mcp.mount_http(mount_path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200) 
