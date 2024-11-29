from attr import dataclass
from typing import Any
import pandas as pd
import datetime as datetime

from pydantic.v1 import BaseModel

from Backend.errors import InvalidTeamInput
from Backend.helpers import get_player, get_position, get_injury, PlayerName
from Backend.scraper import Scraper

name_teamUrl_dict = {
    "bills": "buf",
    "dolphins": "mia",
    "jets": "nyj",
    "patriots": "nwe",
    "steelers": "pit",
    "ravens": "rav",
    "bengals": "cin",
    "browns": "cle",
    "texans": "htx",
    "colts": "clt",
    "titans": "oti",
    "jaguars": "jax",
    "chiefs": "kan",
    "chargers": "sdg",
    "broncos": "den",
    "raiders": "rai",
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
    "cardinals": "crd",
    "rams": "ram",
    "49ers": "sfo"
}

reversed_name_teamUrl_dict = {
    'buf': 'bills',
    'mia': 'dolphins',
    'nyj': 'jets',
    'nwe': 'patriots',
    'pit': 'steelers',
    'rav': 'ravens',
    'cin': 'bengals',
    'cle': 'browns',
    'htx': 'texans',
    'clt': 'colts',
    'oti': 'titans',
    'jax': 'jaguars',
    'kan': 'chiefs',
    'sdg': 'chargers',
    'den': 'broncos',
    'rai': 'raiders',
    'phi': 'eagles',
    'was': 'commanders',
    'dal': 'cowboys',
    'nyg': 'giants',
    'det': 'lions',
    'min': 'vikings',
    'gnb': 'packers',
    'chi': 'bears',
    'atl': 'falcons',
    'tam': 'buccaneers',
    'nor': 'saints',
    'car': 'panthers',
    'sea': 'seahawks',
    'crd': 'cardinals',
    'ram': 'rams',
    'sfo': '49ers'
}


def get_team_name(input_list: list[str]):
    for input in input_list:
        input = input.lower()

        if input in name_teamUrl_dict.values():
            return input

        team = name_teamUrl_dict.get(input)
        if team is not None:
            return team
    return InvalidTeamInput(inputs=input_list)


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

    def __init__(self, input: list[str]):
        self.team = get_team_name(input_list=input)

    def get_team_stats(self, year: int) -> TeamStats:
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
        rank_offense_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[4] if stat.getText() is not ""}
        rank_defense_dict = {stat.attrs["data-stat"]: stat.getText() for stat in rows[5] if stat.getText() is not ""}

        stats = TeamStats(
            team_stat_dict=team_stat_dict,
            opponent_stat_dict=opponent_stat_dict,
            rank_offense_dict=rank_offense_dict,
            rank_defense_dict=rank_defense_dict
        )

        return stats

    @property
    def get_injuries(self) -> list[InjuryMetaData]:
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


    def get_opponent(self, year: int) -> str:
        url = f"https://www.pro-football-reference.com/teams/{self.team}/{year}/gamelog/"
        scraper = Scraper(url=url).grab
        dates = scraper.find_all("td", {"data-stat": "game_date"})
        opps = scraper.find_all("td", {"data-stat": "opp"})

        today = datetime.datetime.now()
        opp_dict = {}
        for opp, date in zip(opps, dates):
            opp_dict[pd.to_datetime(date.getText() + " " + str(today.year), format="%B %d %Y")] = opp.getText()

        closest_date = min(opp_dict.keys(), key=lambda k: abs(k - today))
        closest_value = opp_dict[closest_date]

        return closest_value
