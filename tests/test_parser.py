from utils.parser import _extract_major_from_url, parse_major_list, parse_plan
from dto.plan_response import PlanResponse


def test_extract_major_from_valid_url():
    # Act
    url = "http://www.plan.pwsz.legnica.edu.pl/checkSpecjalnoscStac.php?specjalnosc=s3PAM"

    # Assert
    assert _extract_major_from_url(url) == "s3PAM"

def test_extract_major_from_url_with_multiple_params():
    # Act
    url = "http://example.com/checkSpecjalnoscStac.php?foo=bar&specjalnosc=s2ISL&baz=1"

    # Assert
    assert _extract_major_from_url(url) == "s2ISL"

def test_extract_major_returns_none_on_invalid_page():
    # Act
    url = "http://www.plan.pwsz.legnica.edu.pl/schedule_view.php?id=1"

    # Assert
    assert _extract_major_from_url(url) is None

def test_parse_major_list_success():
    # Arrange
    mock_html = """
    <ul class="accordion">
        <li>
            <a>Informatyka Stacjonarne (s1INF)</a>
            <div>
                <a href="checkSpecjalnoscStac.php?specjalnosc=s1INF">Cały semestr</a>
            </div>
        </li>
        <li>
            <a>Automatyka (s1AUT)</a>
            <div>
                <a href="checkSpecjalnoscStac.php?specjalnosc=s1AUT">Cały semestr</a>
            </div>
        </li>
    </ul>
    """
    # Act
    results = parse_major_list(mock_html)

    # Assert
    assert len(results) == 2
    assert results[0]["major"] == "s1INF"
    assert results[0]["name"] == "Informatyka Stacjonarne (s1INF)"
    assert results[1]["major"] == "s1AUT"


def test_parse_major_list_empty_when_no_accordion():
    # Arrange
    mock_html = "<html><body><div>Brak listy kierunkow</div></body></html>"

    # Act
    results = parse_major_list(mock_html)

    # Assert
    assert results == []

def test_parse_plan_success_single_lesson():
    # Arrange
    mock_html = """
    <table class="TabPlan">
        <tr><td class="nazwaDnia">Wtorek 2026-02-17</td></tr>
        <tr>
            <td class="nazwaSpecjalnosci">s3PAM1(1)</td>
            <td class="nazwaSpecjalnosci">s3PAM1(2)</td>
        </tr>
        <tr>
            <td class="godzina">11:45-13:15</td>
            <td>Sd (sem)</td>
            <td>dr Aleksander Klosow</td>
            <td>A145</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
        </tr>
    </table>
    """

    # Act
    lessons = parse_plan(mock_html)

    # Assert
    assert len(lessons) == 1

    lesson = lessons[0]
    assert isinstance(lesson, PlanResponse)
    assert lesson.day == "Wtorek 2026-02-17"
    assert lesson.hour == "11:45-13:15"
    assert lesson.group == "s3PAM1(1)"
    assert lesson.subject == "Sd (sem)"
    assert lesson.teacher == "dr Aleksander Klosow"
    assert lesson.classroom == "A145"


def test_parse_plan_returns_empty_list_when_no_table():
    # Arrange
    mock_html = "<div>Plan jest chwilowo niedostepny</div>"

    # Act
    lessons = parse_plan(mock_html)

    # Assert
    assert lessons == []