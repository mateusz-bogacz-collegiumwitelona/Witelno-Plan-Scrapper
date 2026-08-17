import httpx
import asyncio
from utils.parser import parse_plan, parse_major_list

BASE_URL = "http://www.plan.pwsz.legnica.edu.pl"

FACULTIES_URLS = [
    f"{BASE_URL}/schedule_view.php?site=show_kierunek.php&id={i}"
    for i in [1, 2, 7, 10, 11, 12]
]

async def get_plan_from_url_async(major: str) -> list:
    url = f"{BASE_URL}/checkSpecjalnoscStac.php?specjalnosc={major}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        response.encoding = 'iso-8859-2'
        html_text = response.text

    return parse_plan(html_text)

async def get_plan(major: str) -> dict:
    data = await get_plan_from_url_async(major)
    return {"data": data}

async def fetch_faculty(client: httpx.AsyncClient, url: str) -> list:
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
        tasks = [fetch_faculty(client, url) for url in FACULTIES_URLS]
        results = await asyncio.gather(*tasks)

        for result in results:
            plans.extend(result)

    return plans

async def get_plans_list() -> dict:
    data = await fetch_all_plans_async()
    return {"data": data}