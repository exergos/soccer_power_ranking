from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# Import models to use in website (database - site connection)
from app_soccer_power_ranking.models import spi_data
from app_soccer_power_ranking.models import elo_data
from app_soccer_power_ranking.models import elo_data_po
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
    standard_ranking_chart_headers = ["Rank","Team","P","G","W","L","T","GF","GA","GD"]
    for i in range(len(standard_ranking.values())):
        standard_ranking_chart_values.append(list())
        standard_ranking_chart_values[i].append(standard_ranking.values()[i]["rank"])
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
    team_finish_elo_po = elo_data_po.objects.all()

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

    elo_chart_po = [[[] for i in repeat(None, 17)] for j in repeat(None, 16)]

    for team in range(len(team_finish_elo_po)):
        elo_chart_po[team][0].append("finish")
        for name, value in team_finish_elo_po[team].get_fields():
            if name == "team":
                elo_chart_po[team][0].append(value)
            for league_positions in range(16):
                if name == "finish_" + str(league_positions+1):
                    elo_chart_po[team][16-league_positions].append(name.strip("finish_"))
                    elo_chart_po[team][16-league_positions].append(decimal.Decimal(value))
                    
    # Django to Javascript gives problems
    # Therefore, convert using jsonEncoder!
    # Do this for every team separate, otherwise problems!
    for team in range(len(spi_chart)):
        spi_chart[team] = json.dumps(spi_chart[team], cls=DecimalEncoder)

    for team in range(len(elo_chart)):
        elo_chart[team] = json.dumps(elo_chart[team], cls=DecimalEncoder)

    for team in range(len(elo_chart_po)):
        elo_chart_po[team] = json.dumps(elo_chart_po[team], cls=DecimalEncoder)


    # ELO past 5 games chart
    dummy = team_finish_elo.values()
    elo_history = list()
    for team in dummy:
        elo_history.append(list())
        for i in range(5):
            elo_history[-1].append(str(team["elo_min" + str(i)]))


    context_dict = {'table_headers' : table_headers,'table_values' : table_values, 'elo_chart': elo_chart, 'elo_chart_po': elo_chart_po, 'elo_history' : elo_history}

    return render(request, 'app_soccer_power_ranking/ranking.html', context_dict)

def game_table(request):
    import datetime
    # Standard Ranking
    # Select Game
    game = game_data.objects.filter(id="10768")

    game_headers = ["Date","Host", "Visitor", "Host Win %", "Tie %", "Visitor Win %"]
    game_values = list()
    game_values.append(game.values()[0]["game_date"])
    game_values.append(game.values()[0]["host"])
    game_values.append(game.values()[0]["visitor"])
    game_values.append(str(round(100*game.values()[0]["host_elo"],0)) + "%")
    game_values.append(str(round(100*game.values()[0]["tie_elo"],0)) + "%")
    game_values.append(str(round(100*game.values()[0]["visitor_elo"],0)) + "%")

    if game.values()[0]["played"] == "1":
        game_headers.append("Host Goals")
        game_headers.append("Visitor Goals")
        game_headers.append("Upset")
        game_headers.append("Excitement")

        game_values.append(str(game.values()[0]["host_goal"]))
        game_values.append(str(game.values()[0]["visitor_goal"]))
        game_values.append(str(round(100*game.values()[0]["upset"],0))+"%")
        game_values.append(str(round(100*game.values()[0]["excitement"],0))+"%")


    # All games played in last season
    games = game_data.objects.filter(game_date__gte = datetime.datetime(2014,7,1)).filter(game_date__lte = datetime.datetime.now())
    games_headers = ["Date","Host", "Visitor", "Host Win %", "Tie %", "Visitor Win %","Host Goals","Visitor Goals","Upset","Excitement"]

    games_values = list()
    for i in range(len(games)): # len(games)
        games_values.append(list())
        dummy = games.values()[i]
        games_values[i].append(dummy["game_date"]) # datetime.datetime.strftime(,"%d/%m/%Y")
        games_values[i].append(dummy["host"])
        games_values[i].append(dummy["visitor"])
        games_values[i].append(str(round(100*dummy["host_elo"],0)) + "%")
        games_values[i].append(str(round(100*dummy["tie_elo"],0)) + "%")
        games_values[i].append(str(round(100*dummy["visitor_elo"],0)) + "%")
        games_values[i].append(str(dummy["host_goal"]))
        games_values[i].append(str(dummy["visitor_goal"]))
        games_values[i].append(str(round(100*dummy["upset"],0))+"%")
        games_values[i].append(str(round(100*dummy["excitement"],0))+"%")


    context_dict = {'game_headers' : game_headers,'game_values' : game_values, 'games_headers' : games_headers, 'games_values' : games_values}

    return render(request, 'app_soccer_power_ranking/games.html', context_dict)



# def chart(request):
#     return(request, 'app_soccer_power_ranking/chart.html')

def chart(request):
    # from django.db import connection
    # cursor = connection.cursor()
    # cursor.execute("SHOW GLOBAL VARIABLES LIKE 'wait_timeout'")
    # print cursor.fetchone()
    # cursor.execute("SET GLOBAL wait_timeout=12345")
    # cursor.execute("SHOW GLOBAL VARIABLES LIKE 'wait_timeout'")
    # print cursor.fetchone()
    # Select Game
    game = game_data.objects.filter(id="10768")
    # Game Chance chart
    # game_chart
    minutes = 90
    game_chart = [[] for i in repeat(None,minutes)]
    game_chart.insert(0,["Minute","Host","Tie","Visitor"])

    for i in range(minutes):
        game_chart[i+1].append(str(i+1))
        game_chart[i+1].append(game.values()[0]["minute_" + str(i+1) + "_host"])
        game_chart[i+1].append(game.values()[0]["minute_" + str(i+1) + "_tie"])
        game_chart[i+1].append(game.values()[0]["minute_" + str(i+1) + "_visitor"])


    # Django to Javascript gives problems
    # Therefore, convert using jsonEncoder!
    # Do this for every team separate, otherwise problems!
    game_chart = json.dumps(game_chart, cls=DecimalEncoder)
    context_dict = {'game_chart': game_chart}

    return render(request, 'app_soccer_power_ranking/chart.html', context_dict)