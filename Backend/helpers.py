from pydantic.v1 import BaseModel


class PlayerName(BaseModel):
    first_name: str
    last_name: str


def get_player(comment_string: str) -> PlayerName:
    player_start = comment_string.find('csk=')  # Locate the "player" attribute
    player_end = comment_string.find('>', player_start)  # Find the closing '<' of the player name
    player = comment_string[player_start + len("csk="): player_end].strip().replace('"', "")
    player_name = PlayerName(
        first_name=player[player.find(",") + 1:],
        last_name=player[0: player.find(",")]
    )
    return player_name


def get_position(comment_string: str):
    position_start = comment_string.find('data-stat="pos" >')
    position_end = comment_string.find("<", position_start)
    position = comment_string[position_start + len('data-stat="pos" >'): position_end].strip()
    return position


def get_injury(comment_string: str):
    position_start = comment_string.find('data-stat="status" >')
    position_end = comment_string.find("<", position_start)
    position = comment_string[position_start + len('data-stat="status" >'): position_end].strip()
    return position
