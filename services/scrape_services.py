import httpx, time
from utils.parser import parse_plan

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

    return  {
        "data": data
    }


