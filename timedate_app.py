from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi_mcp import FastApiMCP
import pytz
from datetime import datetime

app = FastAPI()

class TimeDateRequest(BaseModel):
    timezone: str

class TimeDateResponse(BaseModel):
    datetime: str
    timezone: str

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
                },
            },
            {
                "method": "GET",
                "path": "/api/timezones",
                "description": "List supported IANA timezone names.",
                "example_request": None,
                "example_response": {
                    "count": len(pytz.all_timezones),
                    "timezones": ["Africa/Abidjan", "Africa/Accra", "America/Denver"],
                },
            },
        ],
    }

@app.get("/api/timezones", response_model=TimezonesResponse, tags=["timedate"], operation_id="list_timezones")
async def list_timezones():
    return {"count": len(pytz.all_timezones), "timezones": pytz.all_timezones}

@app.post("/api/timedate", response_model=TimeDateResponse, tags=["timedate"], operation_id="get_time_date")
async def get_time_date(request: TimeDateRequest):
    tz_name = request.timezone
    try:
        tz = pytz.timezone(tz_name)
    except pytz.UnknownTimeZoneError:
        return JSONResponse(status_code=400, content={"error": "Invalid Timezone"})
    now = datetime.now(tz)
    return {"datetime": now.isoformat(), "timezone": tz_name}

# Expose all endpoints via MCP at /mcp
mcp = FastApiMCP(
    app,
    name="Timedate MCP Server",
    description="Provides time and date for a given timezone.",
    describe_all_responses=True,
    describe_full_response_schema=True
)
mcp.mount(mount_path="/mcp")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200) 
