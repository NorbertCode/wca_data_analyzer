import requests
import math


def get_total_pages(url) -> int:
    comp_data = requests.get(url).json()
    return math.ceil(comp_data["total"] / comp_data["pagination"]["size"])


def get_competition_names() -> list[str]:
    competitions = []
    total_pages = get_total_pages("https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/competitions.json")
    for page in range(1, total_pages + 1):
        comp_data = requests.get(f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/competitions-page-{page}.json").json()
        comps_names = [comp["id"] for comp in comp_data["items"]]
        competitions.extend(comps_names)
    return competitions


get_competition_names()
