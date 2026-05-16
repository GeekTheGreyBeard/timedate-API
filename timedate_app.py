from fastapi import FastAPI, Query
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