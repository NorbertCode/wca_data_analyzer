class InvalidDataError(Exception):
    def __init__(self, url):
        super().__init__(f"Failed to load data at url: {url}")
