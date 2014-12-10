# This file will populate database

import os

def populate():
    # Remove previous data in table
    import django
    django.setup()

    # Scrape data from sporza for SPI & ELO algorithms
    import app_soccer_power_ranking.algorithms.sporza as sp
    data_last_season = sp.sporza("Ranking")

    # Scrape data from sporza for game data & game situation
    # Or load from file (pickle)
    import pickle
    data_all = pickle.load(open("app_soccer_power_ranking/algorithms/data/sporza_8_seasons.p", "rb"))  # load from file
    # # Or scrape it back from sporza (TAKES 2 HOURS FOR 25 SEASONS)
    # data = sporza(number_of_seasons = 8)

    # # SPI
    # # Remove previous data
    # spi_data.objects.all().delete()
    #
    # # Generate SPI data
    # import app_soccer_power_ranking.algorithms.SPI_algorithm as spi
    # output_spi = spi.spi(data_last_season)
    #
    # # output_spi is a list of 2 things
    # # [0]:  List of 2 things
    # # [0][0]: Team names of all teams in Jupiler Pro League
    # # [0][1]: Array of size (number of teams x 3)
    # #         [0][1][:,0]: SPI
    # #         [0][1][:,1]: Off Rating
    # #         [0][1][:,2]: Def Rating
    #
    # # [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
    # #       possible league position
    #
    # for i in range(len(output_spi[0][0])): # For every team
    #     # this returns a dict with the property
    #     # name as key and the property val as its value
    #
    #     # d is dictionary of field names and values
    #     d_spi = {'Team' : output_spi[0][0][i],'SPI' : output_spi[0][1][i,0], 'off_rating' : output_spi[0][1][i,1], 'def_rating' : output_spi[0][1][i,2]}
    #     for j in range(16):
    #         d_spi['finish_%s' % (j+1)] = output_spi[1][i,j]
    #
    #     spi_data.objects.create(**d_spi)
    #
    # # ELO
    # # Remove previous data
    # elo_data.objects.all().delete()
    #
    # # Generate ELO data
    # import app_soccer_power_ranking.algorithms.ELO_algorithm as elo
    # output_elo = elo.elo(data_last_season)
    #
    # # output_elo is a list of 2 things
    # # [0]:  List of 2 things
    # # [0][0]: Team names of all teams in Jupiler Pro League
    # # [0][1]: Array of size (number of teams x 3)
    # #         [0][1][:,0]: ELO
    #
    # # [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
    # #       possible league position
    #
    # for i in range(len(output_elo[0][0])): # For every team
    #     # this returns a dict with the property
    #     # name as key and the property val as its value
    #
    #     # d is dictionary of field names and values
    #     d_elo = {'Team' : output_elo[0][0][i],'ELO' : output_elo[0][1][i]}
    #     for j in range(16):
    #         d_elo['finish_%s' % (j+1)] = output_elo[1][i,j]
    #
    #     elo_data.objects.create(**d_elo)

    # Game Data
    # Remove previous data
    game_data.objects.all().delete()

    # Fill table with all this data
    for season in range(len(data_all)): #delta (goal difference)
        for game in range(len(data_all[season])): # game result
            # d is dictionary of field names and values
            d_game_data = data_all[season][game]
            game_data.objects.create(**d_game_data)

    # Game Situations
    # Remove previous data
    game_situations.objects.all().delete()

    # Generate Game Minute data
    from app_soccer_power_ranking.algorithms.GameMinute_algorithm import GameMinute
    output_gs = GameMinute(data_all)

    # output[goal_difference][game_result][minute] as a dict
    # for example: What is the chance the host wins if host is behind 2 goals at the 30 minute mark?
    # output['-2']['1']['30']

    # Fill Database
    for key_gd in output_gs: #delta (goal difference)
        for key_gr in output_gs[key_gd]: # game result
            for key_minute in output_gs[key_gd][key_gr]: #minutes
                # d is dictionary of field names and values
                d_game_situations = {'minute' : int(key_minute.replace("minute_",'')),
                                     'delta' : int(key_gd),
                                     'result' : int(key_gr),
                                     'chance' : output_gs[key_gd][key_gr][key_minute]}
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