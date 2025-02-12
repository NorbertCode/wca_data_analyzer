import errors
import requests
import math
import json


API_URL = "https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/"


def send_request(url: str) -> dict:
    """Sends a GET request and returns its contents as json"""
    request = requests.get(url)
    if request.status_code == 200:
        try:
            return request.json()
        except json.JSONDecodeError as exc:
            raise errors.FailedJsonParsingError(url) from exc
    else:
        raise errors.InvalidResponseError(url, request.status_code)


def get_total_pages(params: str = "") -> int:
    url = f"{API_URL}{params}.json"
    data = send_request(url)
    try:
        return math.ceil(data["total"] / data["pagination"]["size"])
    except (IndexError, ZeroDivisionError) as exc:
        raise errors.FailedReadingPageDataError(url) from exc


def get_json_data(params: str) -> dict:
    """Returns the contents of "items" from all pages"""
    output = []
    url = f"{API_URL}{params}"
    total_pages = get_total_pages(params)
    try:
        if total_pages > 1:
            for page in range(1, total_pages + 1):
                page_data = send_request(f"{url}-page-{page}.json")
                output.extend(page_data["items"])
        else:
            output = send_request(f"{url}.json")["items"]
    except IndexError as exc:
        raise errors.FailedReadingPageDataError(url) from exc

    return output


def get_competition_names(params: str = "") -> list[str]:
    competition_names = []
    comp_data = get_json_data(f"competitions{params}")
    for competition in comp_data:
        competition_names.append(competition["id"])
    return competition_names


def get_competition_solves(competition_names: list[str], params: str = "",
                           output: callable = None,
                           error_output: callable = None) -> list[int]:
    total_solves = []
    for index, comp in enumerate(competition_names):
        try:
            comp_data = get_json_data(f"results/{comp}{params}")
            comp_solves = [solve for result in comp_data for solve in result["solves"]]
            total_solves.extend(comp_solves)
        except (errors.InvalidResponseError, errors.FailedJsonParsingError,
                errors.FailedReadingPageDataError) as exc:
            if error_output is not None:
                error_output(exc)
        if output is not None:
            output(index, len(competition_names))
    return total_solves


def filter_dnfs(solves: list[int]):
    return [solve for solve in solves if solve != -1]
