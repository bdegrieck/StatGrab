import dataclasses

from scraper import Scraper


@dataclasses.dataclass
class TeamOffense:
    year: int
    team: str



    @property
    def get_team_offense_ranks(self):
        scraper = Scraper()
