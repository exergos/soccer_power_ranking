__author__ = 'Exergos'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This file calculates the Soccer Power Index (SPI) for the Jupiler Pro League
# The SPI is one value for every team

# Python 3.3 as Interpreter
# sporza to import sporza data
# Numpy for mathematical use

######################
# What does it return?
######################

# A list of 2 things:
# [0]:  List of 2 things
#       [0][0]: Team names of all teams in Jupiler Pro League
#       [0][1]: Array of size (number of teams x 3)
#               [0][1][:,0]: SPI
#               [0][1][:,1]: Off Rating
#               [0][1][:,2]: Def Rating

# [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
#       possible league position

########################################################################################################################
########################################################################################################################
def spi(input_data, simulations = 10000):
    import numpy as np
    from app_soccer_power_ranking.algorithms.game_to_team import game_to_team
    input_data = game_to_team(input_data)

    # input_data a list of 2 lists
    # [0]:  Team names of all teams in Jupiler Pro League
    # [1]:  Array of size (total games x 5)
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
    # games_not_played = total_games - games_played

    # Calculate SPI using ESPN algorithm
    # Step 1: Assume off_rating & def_rating for every team
    # Based on goals scored in played matches
    goals = np.zeros((number_of_teams, 3))
    for i in range(number_of_teams):
        for j in range(games_played):
            if input_data[1][j, 0] == i:  # Home team
                goals[i, 0] = goals[i, 0] + input_data[1][j, 2]
                goals[i, 1] = goals[i, 1] + input_data[1][j, 3]
                goals[i, 2] = goals[i, 2] + 1
            if input_data[1][j, 1] == i:  # Away team
                goals[i, 0] = goals[i, 0] + input_data[1][j, 3]
                goals[i, 1] = goals[i, 1] + input_data[1][j, 2]
                goals[i, 2] = goals[i, 2] + 1

    off_rating = np.matrix(np.divide(goals[:, 0], goals[:, 2])).transpose()
    def_rating = np.matrix(np.divide(goals[:, 1], goals[:, 2])).transpose()
    # Calculate starting values (to make sure iterative process is converging)
    # Initialize input_data & parameters
    avg_base = 1.37  # Average number of goals scored per team per game in competition (based on historic input_data)
    # Use lists for ags/aga because exact size is unknown beforehand
    ags = [[] for x in range(number_of_teams)]
    aga = [[] for x in range(number_of_teams)]

    for i in range(games_played):  # For every game
        for k in range(number_of_teams):  # Check home and away team
            if input_data[1][i, 0] == k:  # Team was home team for this game
                home_team = k
            if input_data[1][i, 1] == k:  # Team was away team for this game
                away_team = k
        # Home team ags & aga calculation
        ags_dummy = ((input_data[1][i, 2] - def_rating[away_team, 0]) / max(0.25,
                                                                      def_rating[away_team, 0] * 0.424 + 0.548)) * (
                        avg_base * 0.424 + 0.548) + avg_base
        aga_dummy = ((input_data[1][i, 3] - off_rating[away_team, 0]) / max(0.25,
                                                                      off_rating[away_team, 0] * 0.424 + 0.548)) * (
                        avg_base * 0.424 + 0.548) + avg_base
        ags[home_team].append(ags_dummy)
        aga[home_team].append(aga_dummy)

        # Away team ags & aga calculation
        ags_dummy = ((input_data[1][i, 3] - def_rating[home_team, 0]) / max(0.25,
                                                                      def_rating[home_team, 0] * 0.424 + 0.548)) * (
                        avg_base * 0.424 + 0.548) + avg_base
        aga_dummy = ((input_data[1][i, 2] - off_rating[home_team, 0]) / max(0.25,
                                                                      off_rating[home_team, 0] * 0.424 + 0.548)) * (
                        avg_base * 0.424 + 0.548) + avg_base
        ags[away_team].append(ags_dummy)
        aga[away_team].append(aga_dummy)

    # Test if off and def ratings are converging (least squares test)
    for i in range(number_of_teams):
        off_rating[i, 0] = sum(ags[i]) / float(len(ags[i]))
        def_rating[i, 0] = sum(aga[i]) / float(len(aga[i]))

    # Step 2: Calculate Adjusted Goals Scored (AGS) and Adjusted Goals Allowed (AGA) for every game & Iterate to find off and def rating
    error = 0.5
    iter_test = list([error + 1])
    iter_test2 = np.zeros((games_played, 30))
    iter = 0
    while iter_test[iter] > error and iter < 30:

        # Initialize input_data & parameters
        avg_base = 1.37  # Average number of goals scored per team per game in competition (based on historic input_data)
        # Use lists for ags/aga because exact size is unknown beforehand
        ags = [[] for x in range(number_of_teams)]
        aga = [[] for x in range(number_of_teams)]

        for i in range(games_played):  # For every game
            for k in range(number_of_teams):  # Check home and away team
                if input_data[1][i, 0] == k:  # Team was home team for this game
                    home_team = k
                if input_data[1][i, 1] == k:  # Team was away team for this game
                    away_team = k
            # Home team ags & aga calculation
            ags_dummy = ((input_data[1][i, 2] - def_rating[away_team, iter]) / max(0.25, def_rating[
                away_team, iter] * 0.424 + 0.548)) * (avg_base * 0.424 + 0.548) + avg_base
            aga_dummy = ((input_data[1][i, 3] - off_rating[away_team, iter]) / max(0.25, off_rating[
                away_team, iter] * 0.424 + 0.548)) * (avg_base * 0.424 + 0.548) + avg_base
            ags[home_team].append(ags_dummy)
            aga[home_team].append(aga_dummy)

            iter_test2[i, iter] = max(0.25, def_rating[away_team, iter] * 0.424 + 0.548)

            # Away team ags & aga calculation
            ags_dummy = ((input_data[1][i, 3] - def_rating[home_team, iter]) / max(0.25, def_rating[
                home_team, iter] * 0.424 + 0.548)) * (avg_base * 0.424 + 0.548) + avg_base
            aga_dummy = ((input_data[1][i, 2] - off_rating[home_team, iter]) / max(0.25, off_rating[
                home_team, iter] * 0.424 + 0.548)) * (avg_base * 0.424 + 0.548) + avg_base
            ags[away_team].append(ags_dummy)
            aga[away_team].append(aga_dummy)

        # Test if off and def ratings are converging (least squares test)
        iter = iter + 1
        off_rating = np.c_[off_rating, np.zeros(number_of_teams)]
        def_rating = np.c_[def_rating, np.zeros(number_of_teams)]
        for i in range(number_of_teams):
            off_rating[i, iter] = sum(ags[i]) / float(len(ags[i]))
            def_rating[i, iter] = sum(aga[i]) / float(len(aga[i]))

        # iter_test = sum(np.absolute(off_rating[:,iter-1] - off_rating[:, iter]))
        iter_test.append(sum(np.sqrt(np.square(off_rating[:, iter - 1] - off_rating[:, iter]))))

        # EXTRA TEST TO ENSURE CONVERGENCE
        if (iter_test[iter] - iter_test[iter - 1]) < error and iter_test[iter] > error:
            off_rating[:, iter] = (off_rating[:, iter] + off_rating[:, iter - 1]) / 2
            def_rating[:, iter] = (def_rating[:, iter] + def_rating[:, iter - 1]) / 2

    # Step 3: Calculate SPI (Using "A Model Based Ranking System for Soccer Teams" by Wang/Vandebroek
    # First compose OFF & DEF rating into strength factor for every game
    # Strength home team = off_rating(home_team)*def_rating(away_team)
    # Strength away team = off_rating(away_team)*def_rating(home_team)
    # Game result = 1 if home victory, 2 if tie, 3 if away victory
    # Home factor (H): to be determined
    # Tie factor (K): to be determined

    # FOR NOW, ASSUME H = 2.08 and K = 0.905 (see Wang/Vandebroek)
    H = 2.08
    K = 0.905

    # Calculate probabilities for all possible matches in Jupiler Pro League
    # Extend input_data[1] with extra columns
    input_data[1] = np.c_[input_data[1], np.zeros(
        (total_games, 3))]  # 3 extra input_data columns (prob home win, prob tie, prob away win)

    # # Add game already played input_data
    # for i in range(total_games):
    #     input_data[1][0:games_played, (input_data[1].shape[1] - 1)] = 1

    # Calculate probabilities
    for i in range(total_games):
        # Probability for Home Win
        input_data[1][i, 5] = H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[
            input_data[1][i, 1].astype(int), iter] / (
                            H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[input_data[1][i, 1].astype(int), iter] +
                            off_rating[input_data[1][i, 1].astype(int), iter] * def_rating[
                                input_data[1][i, 0].astype(int), iter] + K * np.sqrt(
                                H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[
                                    input_data[1][i, 1].astype(int), iter] * off_rating[input_data[1][i, 1].astype(int), iter] *
                                def_rating[input_data[1][i, 0], iter]))
        # Probability for Tie
        input_data[1][i, 6] = K * np.sqrt(
            H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[input_data[1][i, 1].astype(int), iter] * off_rating[
                input_data[1][i, 1].astype(int), iter] * def_rating[input_data[1][i, 0].astype(int), iter]) / (
                            H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[input_data[1][i, 1].astype(int), iter] +
                            off_rating[input_data[1][i, 1].astype(int), iter] * def_rating[
                                input_data[1][i, 0].astype(int), iter] + K * np.sqrt(
                                H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[
                                    input_data[1][i, 1].astype(int), iter] * off_rating[input_data[1][i, 1].astype(int), iter] *
                                def_rating[input_data[1][i, 0].astype(int), iter]))
        # Probability for Away Win
        input_data[1][i, 7] = off_rating[input_data[1][i, 1].astype(int), iter] * def_rating[input_data[1][i, 0].astype(int), iter] / (
            H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[input_data[1][i, 1].astype(int), iter] + off_rating[
                input_data[1][i, 1].astype(int), iter] * def_rating[input_data[1][i, 0].astype(int), iter] + K * np.sqrt(
                H * off_rating[input_data[1][i, 0].astype(int), iter] * def_rating[input_data[1][i, 1].astype(int), iter] * off_rating[
                    input_data[1][i, 1].astype(int), iter] * def_rating[input_data[1][i, 0].astype(int), iter]))

    # Calculate SPI
    # SPI is always calculated assuming nog games have been played (i.e. a round robin between all teams)
    SPI = np.matrix(np.zeros(number_of_teams)).transpose()
    for i in range(number_of_teams):
        for j in range(total_games):
            if input_data[1][j, 0] == i:  # Home Team
                SPI[i, 0] = SPI[i, 0] + (3 * input_data[1][j, 5] + 1 * input_data[1][j, 6] + 0 * input_data[1][j, 7]) / 3
            if input_data[1][j, 1] == i:  # Away Team
                SPI[i, 0] = SPI[i, 0] + (0 * input_data[1][j, 5] + 1 * input_data[1][j, 6] + 3 * input_data[1][j, 7]) / 3
        SPI[i, 0] = SPI[i, 0] / (2 * total_games / number_of_teams)

    print('SPI Algorithm finished')


    output = list([[input_data[0], np.concatenate((SPI, off_rating[:, iter], def_rating[:, iter]), axis=1)], input_data[1]])

    # Output is a list of 2 items
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

    # This can in the future be used for soccer power ranking app
    # For now only output league ranking distribution data, based on montecarlo simulation:

    from app_soccer_power_ranking.algorithms.montecarlo import montecarlo
    output = montecarlo(output,simulations,actual=1)

    return list([output, input_data])