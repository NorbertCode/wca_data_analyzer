import pytest
import wca_requests as wca_req
import errors


TEST_COMP = "BrizZonSylwesterOpen2022"
TEST_COMP_PARAM = f"results/{TEST_COMP}"


def test_get_total_pages():
    pages = wca_req.get_total_pages(TEST_COMP_PARAM)
    assert pages == 1


def test_get_total_pages_invalid():
    with pytest.raises(errors.InvalidResponseError):
        wca_req.get_total_pages("INVALID_PARAM")


def test_get_json_data():
    data = wca_req.get_json_data(TEST_COMP_PARAM)
    assert len(data) == 145
    for result in data:
        assert type(result) is dict


def test_get_json_data_invalid():
    with pytest.raises(errors.InvalidResponseError):
        wca_req.get_json_data("INVALID_PARAM")


def test_get_competition_names_by_year():
    names = wca_req.get_competition_names("/2022")
    assert len(names) == 1100
    for name in names:
        assert type(name) is str


def test_get_competition_names_by_event():
    names = wca_req.get_competition_names("/333")
    for name in names:
        assert type(name) is str


def test_get_competition_names_invalid():
    with pytest.raises(errors.InvalidResponseError):
        wca_req.get_competition_names("INVALID_PARAM")


def test_get_competition_solves():
    solves = wca_req.get_competition_solves([TEST_COMP], "/444")
    assert len(solves) == 32 * 5  # 32 results, 5 solves each
    for solve in solves:
        assert type(solve) is int


def test_get_competition_solves_output_callback():
    output = []

    def add_to_output(index, total):
        output.append((index, total))

    _ = wca_req.get_competition_solves([TEST_COMP, TEST_COMP], output=add_to_output)

    assert len(output) == 2
    assert output[0] == (0, 2)
    assert output[1] == (1, 2)


def test_get_competition_solves_error_callback():
    error_output = []

    def add_to_err_output(msg):
        error_output.append(msg)

    _ = wca_req.get_competition_solves(["INVALID_PARAM"] * 2,
                                       error_output=add_to_err_output)

    assert len(error_output) == 2
    for error in error_output:
        assert type(error) is errors.InvalidResponseError


def test_filter_dnfs():
    solves = [1, 2, 3, -1, 4]
    filtered = wca_req.filter_dnfs(solves)
    assert len(filtered) == 4
    assert filtered == [1, 2, 3, 4]


def test_filter_dnfs_no_dnfs():
    solves = [1, 2, 3, 4, 5]
    filtered = wca_req.filter_dnfs(solves)
    assert len(filtered) == 5
    assert filtered == [1, 2, 3, 4, 5]
