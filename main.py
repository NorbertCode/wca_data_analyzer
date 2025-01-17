import requests
import json
import math


API_URL = "https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/"


def get_total_pages(url) -> int:
    data = requests.get(url).json()
    return math.ceil(data["total"] / data["pagination"]["size"])


def get_competition_names() -> list[str]:
    competition_names = []
    total_pages = get_total_pages(f"{API_URL}competitions.json")
    for page in range(1, total_pages + 1):
        url = f"{API_URL}competitions-page-{page}.json"
        try:
            comps_data = requests.get(url).json()
            competition_names.extend([comp["id"] for comp in comps_data["items"]])
        except json.JSONDecodeError:
            print(f"Failed to load data at {url}")
    return competition_names


def get_competition_results(competition_names: list[str], event_id: str) -> list[int]:
    solves = []
    for comp in competition_names:
        url = f"{API_URL}results/{comp}/{event_id}.json"
        try:
            comp_data = requests.get(url).json()
            comp_solves = [solve
                           for comp in comp_data["items"]
                           for solve in comp["solves"]]
            solves.extend(comp_solves)
        except json.JSONDecodeError:
            print(f"Failed to load data at {url}")
    return solves


def filter_dnfs(solves: list[int]):
    return [solve for solve in solves if solve != -1]


all_solves = filter_dnfs(get_competition_results(get_competition_names(), "333"))
total_average = sum(all_solves) / len(all_solves)
print(f"Total 3x3 average: {total_average}")
