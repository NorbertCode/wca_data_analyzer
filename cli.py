import wca_requests


def output_fetch_status(current: int, end: int):
    print(f"Loaded competition {current}/{end}")


def average(collection: list[int]):
    return sum(collection) / len(collection)


def to_seconds(value: float):
    return round(value / 100, 2)


comps = wca_requests.get_competition_names("/2024/08/05")
print(f"Fetched {len(comps)} competitions.")
all_solves = wca_requests.get_competition_solves(comps, "/333",
                                                 output_fetch_status, print)
filtered_solves = wca_requests.filter_dnfs(all_solves)
total_average = average(filtered_solves)
print(f"Total 3x3 average: {to_seconds(total_average)}")
