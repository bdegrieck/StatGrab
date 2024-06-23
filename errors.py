


class InvalidResponse(Exception):
    def __init__(self, url, response):
        super().__init__(f"Request for url: {url}, had a response of {response}")
