from fastapi.testclient import TestClient
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