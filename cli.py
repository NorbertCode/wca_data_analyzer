import wca_requests
import argparse


def output_fetch_status(current: int, end: int):
    print(f"Loaded competition {current + 1}/{end}")


def average(collection: list[int]) -> float:
    return sum(collection) / len(collection)


def to_seconds(value: float, decimal: int) -> float:
    return round(value / 100, decimal)


def load_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--competition-parameters", type=str, default="",
                        help="Parameters for competitions, ie. year, year and month," +
                        " or event (for example 333 or 444)")
    parser.add_argument("-s", "--solve-parameters", type=str, default="",
                        help="Parameters for solves from competitions, ie. event" +
                        " (like 333 or 444)")
    return parser.parse_args()


def main(competition_parameters: str, solve_parameters: str):
    comps = wca_requests.get_competition_names(f"/{competition_parameters}")
    print(f"Fetched {len(comps)} competitions.")

    all_solves = wca_requests.get_competition_solves(comps, f"/{solve_parameters}",
                                                    output_fetch_status, print)
    filtered_solves = wca_requests.filter_dnfs(all_solves)
    total_average = average(filtered_solves)
    print(f"Total average: {to_seconds(total_average, 2)}")


if __name__ == "__main__":
    args = load_args()
    main(args.competition_parameters, args.solve_parameters)
