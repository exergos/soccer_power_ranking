from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# Import models to use in website (database - site connection)
from app_soccer_power_ranking.models import spi_data
from app_soccer_power_ranking.models import elo_data
from app_soccer_power_ranking.models import game_data
from app_soccer_power_ranking.models import standings


# To make list of lists that are not copies of each other
from itertools import repeat

# To make Google Charts accept Decimal Data
import json
import decimal

# To make sure transition from Django to Template (javascript) is smooth
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def team_table(request):
    # Standard Ranking
    standard_ranking = standings.objects.all()

    standard_ranking_chart_values = list()
    standard_ranking_chart_headers = ["Team","P","G","W","L","T","GF","GA","GD"]
    for i in range(len(standard_ranking.values())):
        standard_ranking_chart_values.append(list())
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["team"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["points"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["games"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["win"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["loss"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["tie"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["goals_for"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["goals_against"])
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["goal_difference"])

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!

    team_finish_spi = spi_data.objects.all()
    team_finish_elo = elo_data.objects.all()

    # First make table for SPI, off_rating and def_rating
    # Get fields in a list SPI_headers
    # And get all the values in a list of lists (16*16) SPI_values
    spi_table_headers = []
    spi_table_values = [[] for i in repeat(None, 16)]

    elo_table_headers = []
    elo_table_values = [[] for i in repeat(None, 16)]

    for team in range(len(team_finish_spi)):
        for name, value in team_finish_spi[team].get_fields():
            if name == 'team' or name == 'spi' or name == 'off_rating' or name == 'def_rating':
                spi_table_values[team].append(value)
                if team == 0:
                    spi_table_headers.append(name)

    for team in range(len(team_finish_elo)):
        for name, value in team_finish_elo[team].get_fields():
            if name == 'team' or name == 'elo':
                elo_table_values[team].append(value)
                if team == 0:
                    elo_table_headers.append(name)

    # Combine table data in table_headers and table_values
    table_headers = standard_ranking_chart_headers + ["SPI","OR", "DR"] + ["ELO"]
    table_values = list()
    for i in range(len(spi_table_values)):
        table_values.append(list())
        table_values[i] = standard_ranking_chart_values[i] + spi_table_values[i][1:] + elo_table_values[i][1:]

    # Second get all data for chart in a list of lists (16+1,2)
    # Put data in right format to be used by Google Chart in ranking.html
    # i.e.: a list of lists with headers and data (finish position and percentage chance)
    spi_chart = [[[] for i in repeat(None, 17)] for j in repeat(None, 16)]

    for team in range(len(team_finish_spi)):
        spi_chart[team][0].append("finish")
        for name, value in team_finish_spi[team].get_fields():
            if name == "team":
                spi_chart[team][0].append(value)
            for league_positions in range(16):
                if name == "finish_" + str(league_positions+1):
                    spi_chart[team][16-league_positions].append(name.strip("finish_"))
                    spi_chart[team][16-league_positions].append(decimal.Decimal(value))

    elo_chart = [[[] for i in repeat(None, 17)] for j in repeat(None, 16)]

    for team in range(len(team_finish_elo)):
        elo_chart[team][0].append("finish")
        for name, value in team_finish_elo[team].get_fields():
            if name == "team":
                elo_chart[team][0].append(value)
            for league_positions in range(16):
                if name == "finish_" + str(league_positions+1):
                    elo_chart[team][16-league_positions].append(name.strip("finish_"))
                    elo_chart[team][16-league_positions].append(decimal.Decimal(value))

    # Django to Javascript gives problems
    # Therefore, convert using jsonEncoder!
    # Do this for every team separate, otherwise problems!
    for team in range(len(spi_chart)):
        spi_chart[team] = json.dumps(spi_chart[team], cls=DecimalEncoder)

    for team in range(len(elo_chart)):
        elo_chart[team] = json.dumps(elo_chart[team], cls=DecimalEncoder)

    context_dict = {'table_headers' : table_headers,'table_values' : table_values, 'elo_chart': elo_chart}

    return render(request, 'app_soccer_power_ranking/ranking.html', context_dict)

def game_table(request):
    # Standard Ranking
    games = game_data.objects.all()
    games_headers = list(games.values()[0].keys())
    games_values = list()
    for i in range(5): # len(games)
        games_values.append(list(games.values()[i].values()))

    context_dict = {'games_headers' : games_headers,'games_values' : games_values}

    return render(request, 'app_soccer_power_ranking/games.html', context_dict)



def chart(request):
    return(request, 'app_soccer_power_ranking/chart.html')

# def chart(request):
#     # Select Game
#     game = game_data.objects.filter(id="2450")
#     # if int(game.values("host_goal")[0].get("host_goal")) > int(game.values("visitor_goal")[0].get("visitor_goal")):
#     #     end_result = 1
#     # else:
#     #     if int(game.values("host_goal")[0].get("host_goal")) == int(game.values("visitor_goal")[0].get("visitor_goal")):
#     #         end_result = 0
#     #     else:
#     #         end_result = -1
#
#     # Game Chance chart
#     # game_chart
#     minutes = 90
#     game_chart = [[] for i in repeat(None,minutes)]
#     game_chart.insert(0,["Minute","Host","Tie","Visitor"])
#
#     for i in range(minutes):
#         delta_par = game.values("minute_" + str(int(i+1)))[0].get("minute_" + str(int(i+1)))
#         minute_par = i+1
#         game_chart[i+1].append(str(minute_par))
#
#         # Create areachart
#         host_win = game_situations.objects.filter(minute=str(minute_par),delta=delta_par,result=str(1)).values("chance")[0].get("chance")
#         tie = game_situations.objects.filter(minute=str(minute_par),delta=delta_par,result=str(0)).values("chance")[0].get("chance")
#         visitor_win = game_situations.objects.filter(minute=str(minute_par),delta=delta_par,result=str(-1)).values("chance")[0].get("chance")
#         game_chart[i+1].append(host_win)
#         game_chart[i+1].append(tie)
#         game_chart[i+1].append(visitor_win)
#
#     # Django to Javascript gives problems
#     # Therefore, convert using jsonEncoder!
#     # Do this for every team separate, otherwise problems!
#     game_chart = json.dumps(game_chart, cls=DecimalEncoder)
#     context_dict = {'game_chart': game_chart}
#
#     return render(request, 'app_soccer_power_ranking/chart.html', context_dict)