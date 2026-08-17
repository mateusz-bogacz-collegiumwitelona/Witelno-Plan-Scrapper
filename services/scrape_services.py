import httpx
import asyncio
from utils.parser import parse_plan, parse_major_list
from config.redis_config import save_to_cache, get_from_cache

BASE_URL = "http://www.plan.pwsz.legnica.edu.pl"
CACHE_TTL = 3600  # 1h

FACULTIES_URLS = [
    f"{BASE_URL}/schedule_view.php?site=show_kierunek.php&id={i}"
    for i in [1, 2, 7, 10, 11, 12]
]

async def get_plan_from_url_async(major: str) -> list:
    try:
        url = f"{BASE_URL}/checkSpecjalnoscStac.php?specjalnosc={major}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            response.encoding = 'iso-8859-2'
            html_text = response.text

        return parse_plan(html_text)
    except httpx.HTTPError as e:
        print(f"Error retrieving the plan for major {major}: {e}")
        return []

async def get_plan_async(major: str) -> dict:
    try:
        cache_key = f"plan_{major}"
        cached_data = await get_from_cache(cache_key)

        if cached_data:
            return {
                "status": "success",
                "source": "cache",
                "data": cached_data
            }

        data = await get_plan_from_url_async(major)
        await  save_to_cache(cache_key, data, ttl=CACHE_TTL)
        return {
            "status": "success",
            "source": "live",
            "data": data
        }
    except httpx.HTTPError as e:
        return {
            "status": "error",
            "message": f"Error retrieving the plan for major {major}: {e}"
        }


async def fetch_faculty_async(client: httpx.AsyncClient, url: str) -> list:
    try:
        response = await client.get(url)
        response.raise_for_status()
        response.encoding = 'iso-8859-2'
        return parse_major_list(response.text)
    except httpx.HTTPError as e:
        print(f"Error retrieving the department {url}: {e}")
        return []

async def fetch_all_plans_async() -> list:
    plans = []
    async with httpx.AsyncClient() as client:
        tasks = [fetch_faculty_async(client, url) for url in FACULTIES_URLS]
        results = await asyncio.gather(*tasks)

        for result in results:
            plans.extend(result)

    return plans

async def get_plans_list_async() -> dict:
    try:
        cache_key = "all_majors_list"

        cached_data = await get_from_cache(cache_key)
        if cached_data:
            return {
                "status": "success",
                "source": "redis_cache",
                "data": cached_data
            }

        data = await fetch_all_plans_async()
        await save_to_cache(cache_key, data, ttl=CACHE_TTL)

        return {
            "status": "success",
            "source": "live",
            "data": data
        }
    except httpx.HTTPError as e:
        return {
            "status": "error",
            "message": f"Error retrieving the list of majors: {e}"
        }