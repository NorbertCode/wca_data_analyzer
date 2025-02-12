def average(collection: list[int]) -> float:
    return sum(collection) / len(collection)


def to_seconds(milliseconds: float, decimal: int) -> float:
    return round(milliseconds / 100, decimal)
