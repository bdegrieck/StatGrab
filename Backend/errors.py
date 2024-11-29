

class InvalidTeamInput(Exception):
    def __init__(self, inputs: list[str]):
        super().__init__(f"Could not find data for input: {inputs}")


class InvalidResponse(Exception):
    def __init__(self, response: int, url: str):
        super().__init__(f"Got response: {response} for endpoint: {url}")