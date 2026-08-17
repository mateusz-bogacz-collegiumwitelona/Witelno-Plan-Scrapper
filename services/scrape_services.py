import httpx, asyncio
from utils.parser import parse_plan, parse_major_list

FACULTIES_URLS = [
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=1",
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=2",
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=7",
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=10",
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=11",
    "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?site=show_kierunek.php&id=12"
]

def get_plan_from_url(major: str) -> list:
    url = f"http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc={major}"

    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        response.encoding = 'iso-8859-2'
        html_text = response.text

    return parse_plan(html_text)

def get_plan(major: str) -> dict:
    data = get_plan_from_url(major)
    return {"data": data}

async def fetch_facultie(client, url):
    response = await client.get(url)
    response.raise_for_status()
    response.encoding = 'iso-8859-2'
    return parse_major_list(response.text)

async def fetch_all_plans_async() -> list:
    plans = []
    async with httpx.AsyncClient() as client:
        tasks = [fetch_facultie(client, url) for url in FACULTIES_URLS]
        results = await asyncio.gather(*tasks)

        for result in results:
            plans.extend(result)

    return plans

async def get_plans_list() -> dict:
    data = await fetch_all_plans_async()
    return {"data": data}