import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pagination_defaults(mocker):
    mocker.patch("app.services.db_client.get_paginated_appointments", return_value={
        "total": 0, "page": 1, "limit": 10, "data": []
    })

    response = client.get("/appointments")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["page"] == 1
    assert response_data["limit"] == 10
    assert response_data["total"] == 0
    assert response_data["data"] == []


def test_invalid_page_param():
    response = client.get("/appointments?page=0&limit=10")
    assert response.status_code == 400
    assert response.json()["detail"] == "Page must be 1 or greater."


def test_invalid_limit_param():
    response = client.get("/appointments?page=1&limit=101")
    assert response.status_code == 400
    assert response.json()["detail"] == "Limit must be between 1 and 100."


def test_empty_result(mocker):
    mocker.patch("app.services.db_client.get_paginated_appointments", return_value={
        "total": 0, "page": 2, "limit": 10, "data": []
    })

    response = client.get("/appointments?page=2&limit=10")
    assert response.status_code == 200
    assert response.json() == {
        "total": 0, "page": 2, "limit": 10, "data": []
    }


def test_partial_failure_empty_data_nonzero_total(mocker):
    # Mock a scenario where total count is nonzero, but no data is returned (partial service failure)
    mocker.patch("app.services.db_client.get_paginated_appointments", return_value={
        "total": 10, "page": 2, "limit": 10, "data": []
    })

    response = client.get("/appointments?page=2&limit=10")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {
        "total": 10, "page": 2, "limit": 10, "data": []
    }


def test_database_error_handling(mocker):
    # Mock a scenario where the database client raises a 500 error
    mocker.patch("app.services.db_client.get_paginated_appointments", side_effect=ValueError("Database error"))

    response = client.get("/appointments?page=1&limit=10")
    assert response.status_code == 500
    assert response.json()["detail"] == "Database service error."
