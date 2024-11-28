from data import TeamStat

input = "49ers"
instance = TeamStat(input=input)
injuries = instance.get_injuries
print(injuries)
