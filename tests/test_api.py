from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

@patch("routers.plan_controller.get_plans_list_async", new_callable=AsyncMock)
def test_get_available_majors_success(mock_get_list):
    # Arrange
    mock_data = {
        "status": "success",
        "source": "redis_cache",
        "data": [
            {
                "name": "Informatyka",
                "major": "s1INF"
            }
        ]
    }
    mock_get_list.return_value = mock_data

    # Act
    response = client.get("/api/plan/list")

    # Assert
    assert response.status_code == 200
    assert response.json() == mock_data
    mock_get_list.assert_called_once()

@patch("routers.plan_controller.get_plans_list_async", new_callable=AsyncMock)
def test_get_available_majors_handles_exception(mock_get_list):
    # Arrange
    mock_get_list.side_effect = Exception("Critical site error")

    # Act
    response = client.get("/api/plan/list")

    # Assert
    assert response.status_code == 500
    assert response.json() == {"detail": "Error: Critical site error"}

@patch("routers.plan_controller.get_plan_async", new_callable=AsyncMock)
def test_get_major_plan_success(mock_get_plan):
    # Arrange
    mock_data = {
        "status": "success",
        "source": "live",
        "data": [
            {
                "day": "Poniedziałek",
                "subject": "Bazy danych"
            }
        ]
    }
    mock_get_plan.return_value = mock_data

    # Act
    response = client.get("/api/plan/?major=s3PAM")

    # Assert
    assert response.status_code == 200
    assert response.json() == mock_data
    mock_get_plan.assert_called_once_with("s3PAM")

@patch("routers.plan_controller.get_plan_async", new_callable=AsyncMock)
def test_get_major_plan_missing_parameter(mock_get_plan):
    # Act
    response = client.get("/api/plan/")

    # Assert
    # Zauważ
    assert response.status_code == 422
    mock_get_plan.assert_not_called()