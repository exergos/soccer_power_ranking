# This file will populate database
# Includes calculations for SPI (or refers to them)
# (see Tango with Django)

import os

def populate():
    # Remove previous data in table
    import django
    django.setup()
    spi_data.objects.all().delete()
    elo_data.objects.all().delete()
    game_situations.objects.all().delete()

    # SPI CALCULATION HERE
    # Algorithm to get data from sporza and calculate spi and league finish percentage chances
    # Located in map "algorithms" in app_soccer_power_ranking

    # # Load the dictionary back from the pickle file.
    # import pickle
    # data = pickle.load(open("app_soccer_power_ranking/algorithms/data/sporza_last_seasons.p", "rb"))

    # Or scrape it from sporza (just last season, and just the scores)
    import app_soccer_power_ranking.algorithms.sporza as sp
    data = sp.sporza("Ranking")

    # Fill table with all this data
    for key_season in range(data): #delta (goal difference)
        for key_game in range(data[key_season]): # game result
            # d is dictionary of field names and values
            d_game_data = data[key_season][key_game]
            game_data.objects.create(**d_game_data)

    import app_soccer_power_ranking.algorithms.SPI_algorithm as spi
    output_spi = spi.spi(data)
    # A list of 2 things
    # [0]:  List of 2 things
    # [0][0]: Team names of all teams in Jupiler Pro League
    # [0][1]: Array of size (number of teams x 3)
    #         [0][1][:,0]: SPI
    #         [0][1][:,1]: Off Rating
    #         [0][1][:,2]: Def Rating

    # [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
    #       possible league position

    import app_soccer_power_ranking.algorithms.ELO_algorithm as elo
    output_elo = elo.elo(data)
    # A list of 2 things
    # [0]:  List of 2 things
    # [0][0]: Team names of all teams in Jupiler Pro League
    # [0][1]: Array of size (number of teams x 3)
    #         [0][1][:,0]: ELO

    for i in range(len(output_spi[0][0])): # For every team
        # this returns a dict with the property
        # name as key and the property val as its value

        # d is dictionary of field names and values
        d_spi = {'Team' : output_spi[0][0][i],'SPI' : output_spi[0][1][i,0], 'off_rating' : output_spi[0][1][i,1], 'def_rating' : output_spi[0][1][i,2]}
        for j in range(16):
            d_spi['finish_%s' % (j+1)] = output_spi[1][i,j]

        spi_data.objects.create(**d_spi)

        # d is dictionary of field names and values
        d_elo = {'Team' : output_elo[0][0][i],'ELO' : output_elo[0][1][i]}
        for j in range(16):
            d_elo['finish_%s' % (j+1)] = output_elo[1][i,j]

        elo_data.objects.create(**d_elo)

    # Add Game Situation Data
    # Load the dictionary back from the pickle file.
    import pickle
    data = pickle.load(open("app_soccer_power_ranking/algorithms/data/sporza_8_seasons.p", "rb"))

    # If sporza_big(number_of_seasons) is called:
    # output[season][game] =    dict()
    #                           output[season][game]["game_date"]
    #                           output[season][game]["game_hour"]
    #                           output[season][game]["host"]
    #                           output[season][game]["visitor"]
    #                           output[season][game]["host_goal"]
    #                           output[season][game]["visitor_goal"]
    #                           output[season][game]["referee"]
    #                           output[season][game]["stadium"]
    #                           output[season][game]["spectators"]
    #                           output[season][game]["host_goal_data"]
    #                           output[season][game]["visitor_goal_data"]
    #                           output[season][game]["host_yellow_card_data"]
    #                           output[season][game]["visitor_yellow_card_data"]
    #                           output[season][game]["host_red_card_data"]
    #                           output[season][game]["visitor_red_card_data"]
    #                           output[season][game]["host_starting_team"]
    #                           output[season][game]["visitor_starting_team"]
    #                           output[season][game]["host_substitution"]
    #                           output[season][game]["visitor_substitution"]
    #                           output[season][game]["host_manager"]
    #                           output[season][game]["visitor_manager"]
    #                           output[season][game]["minute_x"] with x from 1 tot 90

    # # Or scrape it back from sporza (TAKES 2 HOURS FOR 25 SEASONS)
    # data = sporza(number_of_seasons = 8)

    from app_soccer_power_ranking.algorithms.GameMinute_algorithm import GameMinute
    output = GameMinute(data)

    # output[goal_difference][game_result][minute] as a dict
    # for example: What is the chance the host wins if host is behind 2 goals at the 30 minute mark?
    # output['-2']['1']['30']

    # Fill Database
    for key_gd in range(output): #delta (goal difference)
        for key_gr in range(output[key_gd]): # game result
            for key_minute in range(output[key_gd][key_gr]): #minutes
                # d is dictionary of field names and values
                d_game_situations = {'minute' : int(key_minute.replace("minute_",'')),
                                     'delta' : int(key_gd),
                                     'result' : int(key_gr),
                                     'chance' : output[key_gd][key_gr][key_minute]}
                game_situations.objects.create(**d_game_situations)

# Start execution here!
if __name__ == '__main__':
    print("Starting Soccer Power Ranking database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_soccer_power_ranking.settings')
    from app_soccer_power_ranking.models import spi_data
    from app_soccer_power_ranking.models import elo_data
    from app_soccer_power_ranking.models import game_situations
    from app_soccer_power_ranking.models import game_data

    populate()