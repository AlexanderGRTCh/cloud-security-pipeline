import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
import pytest

@pytest.fixture
def client():
    # Create a test client for the Flask app
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test homepage loads."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Adjust string if needed

def test_ping(client):
    """Test /ping endpoint with default IP."""
    response = client.get("/ping")
    assert response.status_code == 200
    # Look for typical ping response strings (case insensitive)
    assert b"PING" in response.data.upper() or b"bytes from" in response.data.lower()

def test_get_threats(client):
    """Test GET /api/threat returns list of threats."""
    response = client.get("/api/threat")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Starts with 2 threats

def test_post_threat(client):
    """Test POST /api/threat adds a new threat."""
    payload = {"type": "dos", "severity": "low"}
    response = client.post("/api/threat", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["type"] == "dos"
    assert data["severity"] == "low"
    assert "id" in data

def test_post_threat_missing_field(client):
    """Test POST /api/threat with missing fields returns 400."""
    payload = {"type": "dos"}  # Missing 'severity'
    response = client.post("/api/threat", json=payload)
    assert response.status_code == 400 or response.status_code == 422  # Depending on app validation

def test_post_threat_invalid_data(client):
    """Test POST /api/threat with invalid data type returns 400."""
    payload = {"type": 123, "severity": "low"}  # type should be string
    response = client.post("/api/threat", json=payload)
    assert response.status_code == 400 or response.status_code == 422

def test_post_threat_unique_id(client):
    """Test POST /api/threat assigns unique IDs to threats."""
    payload1 = {"type": "malware", "severity": "high"}
    payload2 = {"type": "ransomware", "severity": "medium"}

    response1 = client.post("/api/threat", json=payload1)
    response2 = client.post("/api/threat", json=payload2)

    assert response1.status_code == 201
    assert response2.status_code == 201

    id1 = response1.get_json().get("id")
    id2 = response2.get_json().get("id")

    assert id1 is not None
    assert id2 is not None
    assert id1 != id2  # IDs should be unique

def test_invalid_route(client):
    """Test accessing invalid route returns 404."""
    response = client.get("/invalid-route")
    assert response.status_code == 404

def test_malformed_json(client):
    """Test POST /api/threat with malformed JSON returns 400."""
    response = client.post("/api/threat", data="{bad json", content_type='application/json')
    assert response.status_code == 400


