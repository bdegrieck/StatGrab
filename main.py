from Backend.teamstat import TeamStat, get_team_name

input = "49ers"
instance = TeamStat(input=[input])
opp = instance.get_opponent(year=2024)
splitted_opp = opp.split()
team = get_team_name(input_list=splitted_opp)
print(team)
