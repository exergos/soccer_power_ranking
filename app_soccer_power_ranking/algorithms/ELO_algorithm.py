__author__ = 'Exergos'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This file calculates the ELO Rating for every team of the Jupiler Pro League

# Python 3.3 as Interpreter
# sporza to import sporza data
# Numpy for mathematical use

######################
# What does it return?
######################

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

########################################################################################################################
########################################################################################################################
def elo(input_data, simulations = 10000):
    import numpy as np
    import scipy.stats # For Poisson Distribution, numpy doesn't have it
    from app_soccer_power_ranking.algorithms.game_to_team_data import game_to_team
    input_data = game_to_team(input_data)

    # input_data is a list of 2 lists:
    # [0]:  Team names of all teams in Jupiler Pro League
    # [1]:  Array of size (total games x 4)
    #       [1][:,0]: Home Team (As a number, alphabetically as in [0]
    #       [1][:,1]: Away Team (As a number, alphabetically as in [0]
    #       [1][:,2]: Home Team Goals
    #       [1][:,3]: Away Team Goals
    #       [1][:,4]: Game already played (1 = yes, 0 = no)

    # Define some parameters that will help with reading the code
    number_of_teams = len(input_data[0])
    total_games = len(input_data[1])
    games_played = 0
    for i in range(total_games):
        if input_data[1][i,4] == 1:
            games_played = games_played + 1

    # Calculate ELO using ELO Formula
    # ELO parameters
    elo_start = 1500
    K = 50
    home_field_advantage = 84 # http://clubelo.com/HFA/ for belgium

    # Every team starts off with 1500 before season
    # Calculate through season

    elo_rating_after_game = np.zeros((games_played,number_of_teams))

    for i in range(games_played):
        # Calculate W_home, W_away and G parameter for game
        if input_data[1][i,2] > input_data[1][i,3]: # Home Win
            W_home = 1
            W_away = 0
        if input_data[1][i,2] == input_data[1][i,3]: # Draw
            W_home = 0.5
            W_away = 0.5
        if input_data[1][i,2] < input_data[1][i,3]: # Away Win
            W_home = 0
            W_away = 1

        # G
        if input_data[1][i,2] == input_data[1][i,3] or abs(input_data[1][i,2] - input_data[1][i,3]) == 1: # Draw or 1 goal difference
            G = 1
        else:
            if abs(input_data[1][i,2] - input_data[1][i,3]) == 2: # 2 goals difference
                G = 3/2
            else: # 3 or more goals difference
                G = (11 + abs(input_data[1][i,2] - input_data[1][i,3]))/8

        # Calculate ELO rating AFTER game
        if i == 0: # First game of the season
            # Home Team new ELO rating after game
            W_home_e = 1/(10**(-home_field_advantage/400)+1)
            elo_rating_after_game[i,input_data[1][i,0]] = elo_start + K*G*(W_home-W_home_e)

            # Away Team new ELO rating after game
            W_away_e = 1/(10**(home_field_advantage/400)+1)
            elo_rating_after_game[i,input_data[1][i,1]] = elo_start + K*G*(W_away-W_away_e)
        else:
            # Home Team new ELO rating after game
            W_home_e = 1/(10**(-(elo_rating_after_game[i-1,input_data[1][i,0]]+home_field_advantage-elo_rating_after_game[i-1,input_data[1][i,1]])/400)+1)
            elo_rating_after_game[i,input_data[1][i,0]] = elo_rating_after_game[i-1,input_data[1][i,0]] + K*G*(W_home-W_home_e)

            # Away Team new ELO rating after game
            W_away_e = 1/(10**(-(elo_rating_after_game[i-1,input_data[1][i,1]]-home_field_advantage-elo_rating_after_game[i-1,input_data[1][i,0]])/400)+1)
            elo_rating_after_game[i,input_data[1][i,1]] = elo_rating_after_game[i-1,input_data[1][i,1]] + K*G*(W_away-W_away_e)

        # For every team that didn't play, copy old elo into new spot
        for j in range(number_of_teams):
            if elo_rating_after_game[i,j] == 0:
                if i == 0:
                    elo_rating_after_game[i,j] = elo_start
                else:
                    elo_rating_after_game[i,j] = elo_rating_after_game[i-1,j]

    # Now calculate Win/Loss/Draw expectancy for all games based on actual ELO (after last played game)
    # Expand input_data[1]
    input_data[1] = np.c_[input_data[1], np.zeros((total_games, 3))]  # 3 extra input_data columns (prob home win, prob tie, prob away win)
    for i in range(total_games):
        # Home Team new ELO rating after game
        W_home_e = 1/(10**(-(elo_rating_after_game[games_played-1,input_data[1][i,0]]+home_field_advantage-elo_rating_after_game[games_played-1,input_data[1][i,1]])/400)+1)

        # First estimate expected goals
        # Goals for Home team
        if W_home_e < 0.5:
            home_goals = 0.2 + 1.1*np.sqrt(W_home_e/0.5)
        else:
            home_goals = 1.69 / (1.12*np.sqrt(2 - W_home_e/0.5)+0.18)

        # Goals for the Away team:
        if W_home_e < 0.8:
            away_goals = -0.96 + 1/(0.1+0.44*np.sqrt((W_home_e+0.1)/0.9))
        else:
            away_goals = 0.72*np.sqrt((1 - W_home_e)/0.3)+0.3

        # Now use poisson distribution to determine for each team the chance it scores x goals
        # Combine these for both teams to calculate Win/Loss/Draw expectancy

        for j in range(15):
            for k in range(15):
                if j > k:
                    # Home Win
                   input_data[1][i,5] = input_data[1][i,5] + scipy.stats.distributions.poisson.pmf(j,home_goals)*scipy.stats.distributions.poisson.pmf(k,away_goals)
                if j == k:
                    # Tie
                   input_data[1][i,6] = input_data[1][i,6] + scipy.stats.distributions.poisson.pmf(j,home_goals)*scipy.stats.distributions.poisson.pmf(k,away_goals)
                if j < k:
                    # Away Win
                   input_data[1][i,7] = input_data[1][i,7] + scipy.stats.distributions.poisson.pmf(j,home_goals)*scipy.stats.distributions.poisson.pmf(k,away_goals)

        # Make sure probabilities sum up to 1 (otherwise problem for montecarlo simulation)
        input_data[1][i,5:8] /= input_data[1][i,5:8].sum()

    print('ELO Algorithm finished')

    output = list([[input_data[0], elo_rating_after_game[-1,:]], input_data[1]])

    # Output is a list of 2 items
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

    # This can in the future be used for soccer power ranking app
    # For now only output league ranking distribution data, based on montecarlo simulation:
    from app_soccer_power_ranking.algorithms.montecarlo import montecarlo
    output = montecarlo(output,simulations)

    return output