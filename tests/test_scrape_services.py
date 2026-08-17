import pytest
from unittest.mock import AsyncMock, patch
import httpx
from services.scrape_services import get_plan_async, get_plans_list_async
from dto.plan_response import PlanResponse

pytestmark = pytest.mark.asyncio


@patch("services.scrape_services.get_from_cache")
async def test_get_plan_async_returns_from_cache_if_exists(mock_get_cache):
    # Arrange
    mock_data = [
        {
            "day": "Wtorek 2026-02-17",
            "hour": "11:45-13:15",
            "group": "s3PAM1(1)",
            "subject": "Sd (sem)",
            "teacher": "dr Aleksander Klosow",
            "classroom": "A145"
        }
    ]
    mock_get_cache.return_value = mock_data

    with patch("services.scrape_services.get_plan_from_url_async") as mock_get_url:
        # Act
        result = await get_plan_async("s3PAM")

        # Assert
        assert result["status"] == "success"
        assert result["source"] == "redis_cache"
        assert result["data"] == mock_data

        mock_get_url.assert_not_called()


@patch("services.scrape_services.save_to_cache")
@patch("services.scrape_services.get_from_cache")
@patch("services.scrape_services.get_plan_from_url_async")
async def test_get_plan_async_fetches_live_when_cache_empty(mock_get_url, mock_get_cache, mock_save_cache):
    # Arrange
    mock_get_cache.return_value = None

    mock_lessons = [
        PlanResponse(day="Pon", hour="8:00", group="G1", subject="X", teacher="Y", classroom="Z")
    ]
    mock_get_url.return_value = mock_lessons

    # Act
    result = await get_plan_async("s3PAM")

    # Assert
    assert result["status"] == "success"
    assert result["source"] == "live"
    assert len(result["data"]) == 1

    mock_save_cache.assert_called_once_with("plan_s3PAM", mock_lessons, ttl=3600)

@patch("services.scrape_services.get_from_cache")
async def test_get_plans_list_async_returns_from_cache(mock_get_cache):
    # Arrange
    mock_list = [{"name": "Informatyka", "major": "s1INF"}]
    mock_get_cache.return_value = mock_list

    with patch("services.scrape_services.fetch_all_plans_async") as mock_fetch_all:
        # Act
        result = await get_plans_list_async()

        # Assert
        assert result["status"] == "success"
        assert result["source"] == "redis_cache"
        assert result["data"] == mock_list
        mock_fetch_all.assert_not_called()

async def test_fetch_faculty_async_handles_http_error():
    # Arrange
    mock_client = AsyncMock(spec=httpx.AsyncClient)

    mock_client.get.side_effect = httpx.HTTPStatusError(
        message="Internal Server Error",
        request=httpx.Request("GET", "http://fakeurl"),
        response=httpx.Response(500)
    )

    from services.scrape_services import fetch_faculty_async

    # Act
    result = await fetch_faculty_async(mock_client, "http://fakeurl")

    # Assert
    assert result == []