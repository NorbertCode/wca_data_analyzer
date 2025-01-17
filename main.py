import requests
import math


API_URL = "https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/"


def get_total_pages(url) -> int:
    data = requests.get(url).json()
    return math.ceil(data["total"] / data["pagination"]["size"])


def get_competition_names() -> list[str]:
    competition_names = []
    total_pages = get_total_pages(f"{API_URL}competitions.json")
    for page in range(1, total_pages + 1):
        comps_data = requests.get(f"{API_URL}competitions-page-{page}.json").json()
        competition_names.extend([comp["id"] for comp in comps_data["items"]])
    return competition_names


def get_competition_results(competition_names: list[str], event_id: str) -> list[int]:
    solves = []
    for comp in competition_names:
        comp_data = requests.get(f"{API_URL}results/{comp}/{event_id}.json").json()
        comp_solves = [solve for comp in comp_data["items"] for solve in comp["solves"]]
        solves.extend(comp_solves)
    return solves


def filter_dnfs(solves: list[int]):
    return [solve for solve in solves if solve != -1]


all_solves = get_competition_results(["BrizZonSylwesterOpen2022"], "444")
no_dnf_solves = filter_dnfs(all_solves)
