from flask import Flask, render_template, request

from Backend.teamstat import TeamStats, TeamStat, InjuryMetaData, get_team_name, reversed_name_teamUrl_dict

app = Flask(__name__)


@app.route("/")
def home():
    return render_template(template_name_or_list="home.html")


@app.route("/submit", methods=["POST"])
def submit():
    input = request.form.get("team")
    instance = TeamStat(input=[input])
    input_team_name = get_team_name(input_list=[input])

    input_team_stats: TeamStats = instance.get_team_stats(year=2024)
    input_injuries: list[InjuryMetaData] = instance.get_injuries

    opp = instance.get_opponent(year=2024)
    opp_list = opp.split()
    opponent_team_name = get_team_name(input_list=opp_list)
    opp_instance = TeamStat(input=opp_list)
    opp_injuries: list[InjuryMetaData] = opp_instance.get_injuries

    return render_template(
        template_name_or_list="teamstat.html",
        input_team_name=reversed_name_teamUrl_dict.get(input_team_name).capitalize(),
        opponent_team_name=reversed_name_teamUrl_dict.get(opponent_team_name).capitalize(),
        input_team_stats=input_team_stats.team_stat_dict,
        opp_team_stats=input_team_stats.opponent_stat_dict,
        input_team_rankings_offense=input_team_stats.rank_offense_dict,
        input_team_rankings_defense=input_team_stats.rank_defense_dict,
        input_injuries_list=input_injuries,
        opp_injuries_list=opp_injuries,
        zip=zip
    )

if __name__ == "__main__":
    app.run(debug=True)
