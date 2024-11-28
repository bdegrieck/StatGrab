

class InvalidTeamInput(Exception):
    def __init__(self, input: str):
        super().__init__(f"Could not find data for input: {input}")


class InvalidResponse(Exception):
    def __init__(self, response: int, url: str):
        super().__init__(f"Got response: {response} for endpoint: {url}")