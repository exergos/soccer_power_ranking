from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# Import models to use in website (database - site connection)
from app_soccer_power_ranking.models import spi_data
from app_soccer_power_ranking.models import elo_data

# To make list of lists that are not copies of eachother
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

def index(request):

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
            if name == 'Team' or name == 'SPI' or name == 'off_rating' or name == 'def_rating':
                spi_table_values[team].append(value)
                if team == 0:
                    spi_table_headers.append(name)

    for team in range(len(team_finish_elo)):
        for name, value in team_finish_elo[team].get_fields():
            if name == 'Team' or name == 'ELO':
                elo_table_values[team].append(value)
                if team == 0:
                    elo_table_headers.append(name)
    # Second get all data for chart in a list of lists (16+1,2)
    # Put data in right format to be used by Google Chart in index.html
    # i.e.: a list of lists with headers and data (finish position and percentage chance)
    spi_chart = [[[] for i in repeat(None, 17)] for j in repeat(None, 16)]

    for team in range(len(team_finish_spi)):
        spi_chart[team][0].append("Finish")
        for name, value in team_finish_spi[team].get_fields():
            if name == "Team":
                spi_chart[team][0].append(value)
            for league_positions in range(16):
                if name == "finish_" + str(league_positions+1):
                    spi_chart[team][16-league_positions].append(name.strip("finish_"))
                    spi_chart[team][16-league_positions].append(decimal.Decimal(value))

    elo_chart = [[[] for i in repeat(None, 17)] for j in repeat(None, 16)]

    for team in range(len(team_finish_elo)):
        elo_chart[team][0].append("Finish")
        for name, value in team_finish_elo[team].get_fields():
            if name == "Team":
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

    # # Create links to images (team logos)
    # team_logo_links = list()
    # for i in range(len(spi_table_values)):
    #     # team_logo_links.append("{% static \"static/images/Team Logos/" + spi_table_values[i][0] + ".png\" %}")
    #     team_logo_links.append("images/Team Logos/" + spi_table_values[i][0] + ".png")



    context_dict = {'spi_table_headers': spi_table_headers, 'spi_table_values': spi_table_values, 'spi_chart': spi_chart,
                    'elo_table_headers': elo_table_headers, 'elo_table_values': elo_table_values, 'elo_chart': elo_chart}


    return render(request, 'app_soccer_power_ranking/index.html', context_dict)


