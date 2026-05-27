import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pagination_defaults():
    response = client.get("/appointments")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["page"] == 1
    assert response_data["limit"] == 10
    assert "total" in response_data
    assert "data" in response_data


def test_invalid_page_param():
    response = client.get("/appointments?page=0&limit=10")
    assert response.status_code == 400
    assert response.json()["detail"] == "Page must be 1 or greater."


def test_invalid_limit_param():
    response = client.get("/appointments?page=1&limit=101")
    assert response.status_code == 400
    assert response.json()["detail"] == "Limit must be between 1 and 100."


def test_empty_result():
    # Assuming an empty database for this test
    response = client.get("/appointments?page=2&limit=10")
    assert response.status_code == 200
    assert response.json()["data"] == []
