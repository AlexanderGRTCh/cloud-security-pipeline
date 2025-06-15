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
    # Send GET request to "/"
    response = client.get("/")
    # Check that the response status code is 200 meaning (OK)
    assert response.status_code == 200
    # Check that "Welcome" is in the returned page
    assert b"Welcome" in response.data  # Adjust string if needed

def test_ping(client):
    """Test /ping endpoint with default IP."""
    # Send GET request to "/ping"
    response = client.get("/ping")
    # Should return 200 OK
    assert response.status_code == 200
    # Look for "PING" or "bytes from" in output depends on OS
    assert b"PING" in response.data.upper() or b"bytes from" in response.data.lower()

def test_get_threats(client):
    """Test GET /api/threat returns list of threats."""
    # Call the GET /api/threat endpoint
    response = client.get("/api/threat")
    assert response.status_code == 200
    # Parse response as JSON 
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Starts with 2 threats

def test_post_threat(client):
    """Test POST /api/threat adds a new threat."""
    # Payload = fake threat data
    payload = {"type": "dos", "severity": "low"}
    # Send POST request with JSON data
    response = client.post("/api/threat", json=payload)
    # Should return 201 (created)
    assert response.status_code == 201
    # Check the response matches our data and has an ID
    data = response.get_json()
    assert data["type"] == "dos"
    assert data["severity"] == "low"
    assert "id" in data
