import cli


def test_average():
    assert cli.average([1, 2, 3, 4, 5]) == 3
    assert cli.average([5, 5, 10, 10, 15, 15]) == 10


def test_to_seconds():
    assert cli.to_seconds(1234, 2) == 12.34
    assert cli.to_seconds(1234.5678, 2) == 12.35
