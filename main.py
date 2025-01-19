import requests
import math


API_URL = "https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/"


def get_total_pages(url) -> int:
    data = requests.get(url).json()
    return math.ceil(data["total"] / data["pagination"]["size"])


def get_json_data(params: str) -> dict:
    """Returns the contents of "items" from all pages"""
    output = []
    url = f"{API_URL}{params}"
    total_pages = get_total_pages(f"{url}.json")
    if total_pages > 1:
        for page in range(1, total_pages + 1):
            page_data = requests.get(f"{url}-page-{page}.json").json()
            output.extend(page_data["items"])
    else:
        output = requests.get(f"{url}.json").json()["items"]
    return output


def get_competition_names(params: str = "") -> list[str]:
    competition_names = []
    comp_data = get_json_data(f"competitions{params}")
    for competition in comp_data:
        competition_names.append(competition["id"])
    return competition_names


def get_competition_solves(competition_names: list[str], params: str = "",
                            output: callable = None) -> list[int]:
    total_solves = []
    for comp in competition_names:
        comp_data = get_json_data(f"results/{comp}{params}")
        comp_solves = [solve for result in comp_data for solve in result["solves"]]
        total_solves.extend(comp_solves)
        if output is not None:
            output(competition_names.index(comp), len(competition_names))
    return total_solves


def filter_dnfs(solves: list[int]):
    return [solve for solve in solves if solve != -1]


comps = get_competition_names("/333")[9995:10000]
all_solves = filter_dnfs(get_competition_solves(comps, "/333", lambda curr, end: print(f"{curr}/{end}")))
total_average = sum(all_solves) / len(all_solves)
print(f"Total 3x3 average: {total_average}")
