__author__ = 'Exergos'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This file simulates outcomes for the Jupiler Pro League based on the SPI algorithm
# It uses the a Monte Carlo Simulation
# Parameter "actual":
#       0: It doesn't include games already played
#       1: It does include games already played

# Python 3.4 as Interpreter

######################
# What does it return?
######################
# A list of 2 things
# [0]:  List of 2 things
# [0][0]: Team names of all teams in Jupiler Pro League
#       [0][1]: Array of size (number of teams x 3)
#               [0][1][:,0]: SPI
#               [0][1][:,1]: Off Rating
#               [0][1][:,2]: Def Rating

# [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
#       possible league position

########################################################################################################################
########################################################################################################################

def montecarlo(actual = 0):
    # Argumant actual is defined in function definition so it is optional when calling the function

    # Every action that is not dependent on value "actual" parameter
    from app_soccer_power_ranking.algorithms.SPI_algorithm import spi
    #import SPI_algorithm
    import numpy as np
    import time
    data = spi()
    # spi() returns a list of 2 items
    # [0]:  List of 2 things
    # [0][0]: Team names of all teams in Jupiler Pro League
    #       [0][1]: Array of size (number of teams x 3)
    #               [0][1][:,0]: SPI
    #               [0][1][:,1]: Off Rating
    #               [0][1][:,2]: Def Rating

    # [1]:  Array of size ((games played + games not played) x 8)
    #       [1][:,0]: Home Team (As a number, alphabetically as in [0]
    #       [1][:,1]: Away Team (As a number, alphabetically as in [0]
    #       [1][:,2]: Home Team Goals
    #       [1][:,3]: Away Team Goals
    #       [1][:,4]: Probability of Home Win
    #       [1][:,5]: Probability of Tie
    #       [1][:,6]: Probability of Away Win
    #       [1][:,7]: Game already played? (1 = yes, 0 = no)

    # Define some parameters to make code more readable
    total_games = len(data[1])  # All possible games in a season
    number_of_teams = len(data[0][0])


    # Initialize parameters for Monte Carlo Simulation
    simulations = 10000
    simulation = 0
    simulation_matrix = np.zeros((total_games, simulations))

    # Monte Carlo Simulation
    # Simulate every game in a season, and this "simulations" times
    # This data can then be used to generate statistical output

    sim_start = time.time()
    while simulation < simulations:
        for i in range(total_games):  # total games
            simulation_matrix[i, simulation] = np.random.choice([0, 1, 2], p=data[1][i, 4:7])
        simulation += 1
    sim_end = time.time()

    print(sim_end - sim_start)

    # Adjust simulation_matrix for games already played (only if "actual" parameter = 1)!!
    if actual == 1:
        for i in range(total_games):
            if data[1][i,7] == 1:  # Game already played
                if data[1][i,2] > data[1][i,3]:  # Home Win
                    simulation_matrix[i,:] = np.matrix(np.zeros(simulations))
                if data[1][i,2] == data[1][i,3]:  # Tie
                    simulation_matrix[i,:] = np.matrix(np.ones(simulations))
                if data[1][i,2] < data[1][i,3]:  # Away Win
                    simulation_matrix[i,:] = np.matrix(2*np.ones(simulations))

    # Generate Output based on Monte Carlo Simulation
    # Determine number of points & league position for every team in every simulation

    sim_start = time.time()
    # points is matrix of size number_of_teams x simulation
    # unsorted (teams alphabetically) points for every team in every season
    points = np.zeros((number_of_teams, simulations))

    # league_ranking is matrix of size number_of_teams x simulation
    # sorted (descending) index of team on that position
    league_ranking = np.zeros((number_of_teams, simulations))
    for i in range(simulations):
        for j in range(total_games):
            for k in range(number_of_teams):
                if data[1][j, 0] == k:  # Home Team
                    if simulation_matrix[j, i] == 0:  # Home Team Victory
                        points[k, i] += 3
                    if simulation_matrix[j, i] == 1:  # Tie
                        points[k, i] += 1
                    if simulation_matrix[j, i] == 2:  # Away Team Victory
                        points[k, i] += 0
                if data[1][j, 1] == k:  # Away team
                    if simulation_matrix[j, i] == 0:  # Home Team Victory
                        points[k, i] += 0
                    if simulation_matrix[j, i] == 1:  # Tie
                        points[k, i] += 1
                    if simulation_matrix[j, i] == 2:  # Away Team Victory
                        points[k, i] += 3
        league_ranking[:, i] = np.argsort(points[:, i])[::-1]  # Best Team index [0], Worst team index [15]

    sim_end = time.time()
    print(sim_end - sim_start)

    # Average amount of points for every team
    # number_of_teams (ordered alphabetically) x 1 matrix
    points_avg = np.sum(points, axis=1) / simulations

    # Percentage chance to end up in certain league position
    # number_of_teams (ordered alphabetically) x number_of_teams (ranking)
    league_ranking_distribution = np.zeros((number_of_teams, number_of_teams))
    for i in range(number_of_teams):
        # Some teams may not get simulated on every position
        # For example a very good team might never simulate in last place
        # For that reason we have to check this and extend array if necessary (with 0 values)
        possible_positions_i = np.unique(np.where(league_ranking == i)[0])
        amount_per_position_i = np.bincount(np.where(league_ranking == i)[0]) / simulations
        # Remove zeros from amount_per_position_i
        amount_per_position_i = amount_per_position_i[amount_per_position_i != 0]
        for j in range(len(possible_positions_i)):
            league_ranking_distribution[i, possible_positions_i[j]] = amount_per_position_i[j]

    # Round all numbers to 2 digits behind comma
    data[0][1] = np.around(data[0][1],2)
    league_ranking_distribution = np.around(league_ranking_distribution,2)

    return list([data[0],league_ranking_distribution])