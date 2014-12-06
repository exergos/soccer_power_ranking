__author__ = 'Exergos'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This file simulates outcomes for the Jupiler Pro League based on the SPI algorithm and the ELO algorithm
# It uses the a Monte Carlo Simulation

# Python 3.3 as Interpreter

######################
# What does it return?
######################
# A dict of 2 things:
# "spi":
# A list of 2 things:
# [0]:  List of 2 things
#       [0][0]: Team names of all teams in Jupiler Pro League
#       [0][1]: Array of size (number of teams x 3)
#               [0][1][:,0]: SPI
#               [0][1][:,1]: Off Rating
#               [0][1][:,2]: Def Rating

# [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
#       possible league position

# "elo":
# A list of 2 things:
# [0]:  List of 2 things
#       [0][0]: Team names of all teams in Jupiler Pro League
#       [0][1]: List of ELO rating for every team (after last played game)

# [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
#       possible league position

########################################################################################################################
########################################################################################################################

def montecarlo(actual = 0):
    # Argument actual is defined in function definition so it is optional when calling the function

    # Every action that is not dependent on value "actual" parameter
    from app_soccer_power_ranking.algorithms.SPI_algorithm import spi
    from app_soccer_power_ranking.algorithms.ELO_algorithm import elo
    #import SPI_algorithm
    import numpy as np
    import time

    data_spi = spi()
    # Returns a list of 2 items
    # [0]:  List of 2 things
    # [0][1]: Team names of all teams in Jupiler Pro League
    #       [0][2]: Array of size (number of teams x 3)
    #               [0][2][:,0]: SPI
    #               [0][2][:,1]: Off Rating
    #               [0][2][:,2]: Def Rating

    # [1]:  Array of size ((games played + games not played) x 8)
    #       [1][:,0]: Home Team (As a number, alphabetically as in [0]
    #       [1][:,1]: Away Team (As a number, alphabetically as in [0]
    #       [1][:,2]: Home Team Goals
    #       [1][:,3]: Away Team Goals
    #       [1][:,4]: Game already played? (1 = yes, 0 = no)
    #       [1][:,5]: Probability of Home Win
    #       [1][:,6]: Probability of Tie
    #       [1][:,7]: Probability of Away Win

    data_elo = elo()
    # Returns a list of 2 items
    # [0]:  List of 2 things
    #       [0][0]: Team names of all teams in Jupiler Pro League
    #       [0][1]: List of ELO rating for every team (after last played game)

    # [1]:  Array of size ((games played + games not played) x 8)
    #       [1][:,0]: Home Team (As a number, alphabetically as in [0]
    #       [1][:,1]: Away Team (As a number, alphabetically as in [0]
    #       [1][:,2]: Home Team Goals
    #       [1][:,3]: Away Team Goals
    #       [1][:,4]: Game already played? (1 = yes, 0 = no)
    #       [1][:,5]: Probability of Home Win
    #       [1][:,6]: Probability of Tie
    #       [1][:,7]: Probability of Away Win


    # Define some parameters to make code more readable
    total_games = len(data_spi[1])  # All possible games in a season
    number_of_teams = len(data_spi[0][0])

    # Initialize parameters for Monte Carlo Simulation
    simulations = 10000
    simulation = 0
    simulation_matrix_spi = np.zeros((total_games, simulations))
    simulation_matrix_elo = np.zeros((total_games, simulations))

    # Monte Carlo Simulation
    # Simulate every game in a season, and this "simulations" times
    # This data_spi can then be used to generate statistical output

    sim_start = time.time()
    while simulation < simulations:
        for i in range(total_games):  # total games
            simulation_matrix_spi[i, simulation] = np.random.choice([0, 1, 2], p=data_spi[1][i, 5:8])
            simulation_matrix_elo[i, simulation] = np.random.choice([0, 1, 2], p=data_elo[1][i, 5:8])
        simulation += 1
    sim_end = time.time()

    print('Montecarlo Simulation finished in', sim_end - sim_start, 'seconds')

    # Adjust simulation_matrix for games already played (only if "actual" parameter = 1)!!
    # 0 for Home Win, 1 for Tie, 2 for Away Win
    if actual == 1:
        for i in range(total_games):
            if data_spi[1][i,7] == 1:  # Game already played
                if data_spi[1][i,2] > data_spi[1][i,3]:  # Home Win
                    simulation_matrix_spi[i,:] = np.matrix(np.zeros(simulations))
                    simulation_matrix_elo[i,:] = np.matrix(np.zeros(simulations))
                if data_spi[1][i,2] == data_spi[1][i,3]:  # Tie
                    simulation_matrix_spi[i,:] = np.matrix(np.ones(simulations))
                    simulation_matrix_elo[i,:] = np.matrix(np.ones(simulations))
                if data_spi[1][i,2] < data_spi[1][i,3]:  # Away Win
                    simulation_matrix_spi[i,:] = np.matrix(2*np.ones(simulations))
                    simulation_matrix_elo[i,:] = np.matrix(2*np.ones(simulations))

    # Generate Output based on Monte Carlo Simulation
    # Determine number of points & league position for every team in every simulation

    sim_start = time.time()
    # points is matrix of size number_of_teams x simulation
    # unsorted (teams alphabetically) points for every team in every season
    points_spi = np.zeros((number_of_teams, simulations))
    points_elo = np.zeros((number_of_teams, simulations))

    # league_ranking is matrix of size number_of_teams x simulation
    # sorted (descending) index of team on that position
    league_ranking_spi = np.zeros((number_of_teams, simulations))
    league_ranking_elo = np.zeros((number_of_teams, simulations))
    for i in range(simulations):
        for j in range(total_games):
            for k in range(number_of_teams):
                # SPI
                if data_spi[1][j, 0] == k:  # Home Team
                    if simulation_matrix_spi[j, i] == 0:  # Home Team Victory
                        points_spi[k, i] += 3
                    if simulation_matrix_spi[j, i] == 1:  # Tie
                        points_spi[k, i] += 1
                    if simulation_matrix_spi[j, i] == 2:  # Away Team Victory
                        points_spi[k, i] += 0
                if data_spi[1][j, 1] == k:  # Away team
                    if simulation_matrix_spi[j, i] == 0:  # Home Team Victory
                        points_spi[k, i] += 0
                    if simulation_matrix_spi[j, i] == 1:  # Tie
                        points_spi[k, i] += 1
                    if simulation_matrix_spi[j, i] == 2:  # Away Team Victory
                        points_spi[k, i] += 3
                        # ELO
                if data_elo[1][j, 0] == k:  # Home Team
                    if simulation_matrix_elo[j, i] == 0:  # Home Team Victory
                        points_elo[k, i] += 3
                    if simulation_matrix_elo[j, i] == 1:  # Tie
                        points_elo[k, i] += 1
                    if simulation_matrix_elo[j, i] == 2:  # Away Team Victory
                        points_elo[k, i] += 0
                if data_elo[1][j, 1] == k:  # Away team
                    if simulation_matrix_elo[j, i] == 0:  # Home Team Victory
                        points_elo[k, i] += 0
                    if simulation_matrix_elo[j, i] == 1:  # Tie
                        points_elo[k, i] += 1
                    if simulation_matrix_elo[j, i] == 2:  # Away Team Victory
                        points_elo[k, i] += 3
        league_ranking_spi[:, i] = np.argsort(points_spi[:, i])[::-1]  # Best Team index [0], Worst team index [15]
        league_ranking_elo[:, i] = np.argsort(points_elo[:, i])[::-1]  # Best Team index [0], Worst team index [15]

    sim_end = time.time()
    print('League Ranking Distribution finished in ', sim_end - sim_start,'seconds')

    # Average amount of points for every team
    # number_of_teams (ordered alphabetically) x 1 matrix
    points_spi_avg = np.sum(points_spi, axis=1) / simulations
    points_elo_avg = np.sum(points_elo, axis=1) / simulations

    # Percentage chance to end up in certain league position
    # number_of_teams (ordered alphabetically) x number_of_teams (ranking)
    league_ranking_distribution_spi = np.zeros((number_of_teams, number_of_teams))
    league_ranking_distribution_elo = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        # Some teams may not get simulated on every position
        # For example a very good team might never simulate in last place
        # For that reason we have to check this and extend array if necessary (with 0 values)
        #SPI
        possible_positions_i_spi = np.unique(np.where(league_ranking_spi == i)[0])
        amount_per_position_i_spi = np.bincount(np.where(league_ranking_spi == i)[0]) / simulations
        # Remove zeros from amount_per_position_i
        amount_per_position_i_spi = amount_per_position_i_spi[amount_per_position_i_spi != 0]
        for j in range(len(possible_positions_i_spi)):
            league_ranking_distribution_spi[i, possible_positions_i_spi[j]] = amount_per_position_i_spi[j]

        #ELO
        possible_positions_i_elo = np.unique(np.where(league_ranking_elo == i)[0])
        amount_per_position_i_elo = np.bincount(np.where(league_ranking_elo == i)[0]) / simulations
        # Remove zeros from amount_per_position_i
        amount_per_position_i_elo = amount_per_position_i_elo[amount_per_position_i_elo != 0]
        for j in range(len(possible_positions_i_elo)):
            league_ranking_distribution_elo[i, possible_positions_i_elo[j]] = amount_per_position_i_elo[j]

    # Round all numbers to 2 digits behind comma
    data_spi[0][1] = np.around(data_spi[0][1],2)
    data_elo[0][1] = np.around(data_elo[0][1],2)
    league_ranking_distribution_spi = np.around(league_ranking_distribution_spi,2)
    league_ranking_distribution_elo = np.around(league_ranking_distribution_elo,2)

    return {'spi' : list([data_spi[0],league_ranking_distribution_spi]), 'elo' : list([data_elo[0],league_ranking_distribution_elo])}