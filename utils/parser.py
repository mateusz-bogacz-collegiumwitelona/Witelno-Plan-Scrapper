from typing import List, Optional
import urllib.parse as urlparse
from bs4 import BeautifulSoup
from bs4.element import Tag
from dto.plan_response import PlanResponse


def _parse_lesson_chunk(cells: List[Tag], group_name: str, day: str, hour: str) -> Optional[PlanResponse]:
    subject = cells[0].get_text(strip=True)
    if subject in ['-', '']:
        return None

    teacher = cells[1].get_text(strip=True)
    room = cells[2].get_text(strip=True)

    return PlanResponse(
        day=day,
        hour=hour,
        group=group_name,
        subject=subject,
        teacher=teacher,
        classroom=room
    )


def _extract_major_from_url(url: str) -> Optional[str]:
    if 'checkSpecjalnoscStac.php' not in url:
        return None

    parsed_url = urlparse.urlparse(url)
    params = urlparse.parse_qs(parsed_url.query)

    return params.get('specjalnosc', [None])[0]


def parse_plan(html_content: str) -> List[PlanResponse]:
    soup = BeautifulSoup(html_content, "html.parser")
    plan_table = soup.find("table", class_="TabPlan")

    if not plan_table:
        return []

    result = []
    current_day = None
    current_groups = []

    for row in plan_table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue

        day_cell = row.find("td", class_="nazwaDnia")
        if day_cell:
            current_day = day_cell.get_text(strip=True)
            continue

        if row.find("td", class_="nazwaSpecjalnosci"):
            current_groups = [
                td.get_text(strip=True) for td in cells
                if td.has_attr("class") and "nazwaSpecjalnosci" in td["class"]
            ]
            continue

        hour_cell = row.find("td", class_="godzina")
        if hour_cell and current_groups:
            hour = hour_cell.get_text(strip=True)
            data_cells = cells[1:]

            if len(data_cells) == len(current_groups) * 3:
                for i, group in enumerate(current_groups):
                    chunk = data_cells[i * 3: (i + 1) * 3]
                    lesson = _parse_lesson_chunk(chunk, group, current_day, hour)

                    if lesson:
                        result.append(lesson)

    return result


def parse_major_list(html_text: str) -> list:
    soup = BeautifulSoup(html_text, "html.parser")
    accordion = soup.find("ul", class_="accordion")

    plans = []
    if not accordion:
        return plans

    for li in accordion.find_all("li"):
        header_a = li.find("a")
        div = li.find("div")

        if not header_a or not div:
            continue

        name = header_a.get_text(strip=True)

        for a in div.find_all('a'):
            major = _extract_major_from_url(a.get('href', ''))
            if major:
                plans.append({"name": name, "major": major})
                break

    return plans