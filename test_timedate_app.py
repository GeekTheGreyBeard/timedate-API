from fastapi.testclient import TestClient
import pytz
from timedate_app import app

client = TestClient(app)

def test_valid_timezone():
    response = client.post("/api/timedate", json={"timezone": "Europe/London"})
    assert response.status_code == 200
    data = response.json()
    assert "datetime" in data
    assert data["timezone"] == "Europe/London"

def test_invalid_timezone():
    response = client.post("/api/timedate", json={"timezone": "Invalid/Zone"})
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "Invalid Timezone"

def test_usage_endpoint_describes_examples():
    response = client.get("/api/usage")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Timedate API"
    paths = {endpoint["path"] for endpoint in data["endpoints"]}
    assert "/api/timedate" in paths
    assert "/api/timezones" in paths

def test_timezones_endpoint_lists_supported_timezones():
    response = client.get("/api/timezones")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == len(pytz.all_timezones)
    assert "Europe/London" in data["timezones"]
    assert "America/Denver" in data["timezones"]
