class InvalidResponseError(Exception):
    def __init__(self, url, code):
        super().__init__(f"Failed to load data with code {code} at url: {url}")


class FailedJsonParsingError(Exception):
    def __init__(self, url):
        super().__init__(f"Failed to parse json data at url: {url}")


class FailedReadingPageDataError(Exception):
    def __init__(self, url):
        super().__init__(f"Failed reading page data at url: {url}")
