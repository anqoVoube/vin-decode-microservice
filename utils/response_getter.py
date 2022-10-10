import requests


class ResponseDataGetter:
    """
    Sends request and fetches the response data

    Args:
        `url`: URL path for request
    """

    def __init__(self, url: str):
        self.url = url

    def fetch(self):
        return requests.get(url=self.url).text
