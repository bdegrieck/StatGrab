from attr import dataclass
from typing import Any

from pydantic.v1 import BaseModel

from errors import InvalidTeamInput
from helpers import get_player, get_position, get_injury, PlayerName
from scraper import Scraper


def get_team_name(input: str):
    input = input.lower()
    name_teamUrl_dict = {
        "bills": "buf",
        "dolphins": "mia",
        "jets": "nyj",
        "patriots": "nwe",
        "steelers": "pit",
        "ravens": "bal",
        "bengals": "cin",
        "browns": "cle",
        "texans": "hou",
        "colts": "ind",
        "titans": "ten",
        "jaguars": "jax",
        "chiefs": "kan",
        "chargers": "lac",
        "broncos": "den",
        "raiders": "lvr",
        "eagles": "phi",
        "commanders": "was",
        "cowboys": "dal",
        "giants": "nyg",
        "lions": "det",
        "vikings": "min",
        "packers": "gnb",
        "bears": "chi",
        "falcons": "atl",
        "buccaneers": "tam",
        "saints": "nor",
        "panthers": "car",
        "seahawks": "sea",
        "cardinals": "ari",
        "rams": "lar",
        "49ers": "sfo"
    }

    team = name_teamUrl_dict.get(input)
    if team is None:
        raise InvalidTeamInput(input=input)
    return team


@dataclass
class TeamStats:
    team_stat_dict: dict[str, Any]
    opponent_stat_dict: dict[str, Any]
    rank_offense_dict: dict[str, Any]
    rank_defense_dict: dict[str, Any]


class InjuryMetaData(BaseModel):
    player: PlayerName
    injury: str
    position: str


class TeamStat:

    def __init__(self, input: str):
        self.team = get_team_name(input=input)

    def get_team_stats(self, year: str) -> TeamStats:
        """
        :param year: team string year for url
        :return: Object of dictionaries of stats for a team
        """

        url = f"https://www.pro-football-reference.com/teams/{self.team}/{year}.htm"

        scraper = Scraper(url=url).grab
        table = scraper.find(id="all_team_stats")
        rows = table.find_all("tr")

        team_stat_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[2]}
        opponent_stat_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[3]}
        rank_offense_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[4]}
        rank_defense_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[5]}

        stats = TeamStats(
            team_stat_dict=team_stat_dict,
            opponent_stat_dict=opponent_stat_dict,
            rank_offense_dict=rank_offense_dict,
            rank_defense_dict=rank_defense_dict
        )

        return stats

    @property
    def get_injuries(self):
        url = f"https://www.pro-football-reference.com/teams/{self.team}/{2024}.htm"
        scraper = Scraper(url=url).grab
        content = scraper.find(id=f"all_{self.team}_injury_report")
        injury_report = content.contents[4].strip().split('<th scope="row"')

        injuries = []
        for injury_data in injury_report[1:]:
            injuries.append(InjuryMetaData(
                    player=get_player(comment_string=injury_data),
                    position=get_position(comment_string=injury_data),
                    injury=get_injury(comment_string=injury_data)
                )
            )
        return injuries
