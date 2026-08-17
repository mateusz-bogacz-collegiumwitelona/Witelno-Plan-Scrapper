from typing import List

from bs4 import BeautifulSoup
from dto.plan_response import PlanResponse

def parse_plan(html_content: str) -> List[PlanResponse]:
    soup = BeautifulSoup(html_content, "html.parser")
    plan_table = soup.find("table", class_="TabPlan")

    if not plan_table:
        return

    result = []
    current_day = None
    current_groups = []

    for row in plan_table.find_all("tr"):
        cell = row.find_all("td")
        if not cell:
            continue

        day_cell = row.find_all("td", class_="nazwaDnia")
        if day_cell:
            current_day = day_cell[0].get_text(strip=True)
            continue

        if row.find("td", class_="nazwaSpecjalnosci"):
            current_groups = [td.get_text(strip=True) for td in cell if td.has_attr("class") and "nazwaSpecjalnosci" in td["class"]]
            continue

        houre_cell = row.find("td", class_="godzina")
        if houre_cell:
            houre = houre_cell.get_text(strip=True)
            data_class = cell[1:]

            if current_groups and len(data_class) == len(current_groups) * 3:
                for i in range(len(current_groups)):
                    subject = data_class[i * 3].get_text(strip=True)
                    teacher = data_class[i * 3 + 1].get_text(strip=True)
                    room = data_class[i * 3 + 2].get_text(strip=True)

                    if subject not in ['-', '']:
                        result.append(PlanResponse(
                            day=current_day,
                            hour=houre,
                            group=current_groups[i],
                            subject=subject,
                            teacher=teacher,
                            classroom=room
                        ))
    return result

