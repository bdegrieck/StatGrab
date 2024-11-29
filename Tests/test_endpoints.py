import requests


class TestEndpoints:

    def test_endpoints(self):
        team = "buf"
        endpoint = f"https://www.pro-football-reference.com/teams/{team}/{2024}.htm"
        response = requests.get(endpoint)
        assert response.status_code == 200