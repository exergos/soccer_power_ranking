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
# A list of 2 things:
# [0]:  List of 2 things
#       [0][0]: Team names of all teams in Jupiler Pro League
#       [0][1]: Array of size (number of teams x 3)
#               [0][1][:,0]: SPI
#               [0][1][:,1]: Off Rating
#               [0][1][:,2]: Def Rating
# Or, in case of ELO simulation:
#       [0][1]: Array of size (number of teams x 1)
#               [0][1][:,0]: ELO

# [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
#       possible league position

########################################################################################################################
########################################################################################################################

def montecarlo(data, simulations, actual = 0):
    # Argument actual is defined in function definition so it is optional when calling the function
    simulations_po = 100
    import numpy as np
    import time
    # data
    # # [0]:  List of 2 things
    # #       [0][0]: Team names of all teams in Jupiler Pro League
    # #       [0][1]: List of ELO/(SPI,off_rating,def_rating) rating for every team (after last played game)
    #
    # # [1]:  Array of size ((games played + games not played) x 8)
    # #       [1][:,0]: Home Team (As a number, alphabetically as in [0]
    # #       [1][:,1]: Away Team (As a number, alphabetically as in [0]
    # #       [1][:,2]: Home Team Goals
    # #       [1][:,3]: Away Team Goals
    # #       [1][:,4]: Game already played? (1 = yes, 0 = no)
    # #       [1][:,5]: Probability of Home Win
    # #       [1][:,6]: Probability of Tie
    # #       [1][:,7]: Probability of Away Win

    # Define some parameters to make code more readable
    total_games = len(data[1])  # All possible games in a season
    number_of_teams = len(data[0][0])

    # Initialize parameters for Monte Carlo Simulation
    simulation = 0
    simulation_matrix = np.zeros((total_games, simulations))

    # Monte Carlo Simulation
    # Simulate every game in a season, and this "simulations" times
    # This data can then be used to generate statistical output

    sim_start = time.time()
    while simulation < simulations:
        for i in range(total_games):  # total games
            simulation_matrix[i, simulation] = np.random.choice([0, 1, 2], p=data[1][i, 5:8])
        simulation += 1
    sim_end = time.time()

    print('Regular Season Montecarlo Simulation finished in', round(sim_end - sim_start,0), 'seconds, taking ' + str(simulations) + ' simulations')

    # Adjust simulation_matrix for games already played (only if "actual" parameter = 1)!!
    # 0 for Home Win, 1 for Tie, 2 for Away Win
    simulation_matrix_regular = np.zeros((total_games, simulations))
    if actual == 1:
        for i in range(total_games):
            if data[1][i,7] == 1:  # Game already played
                if data[1][i,2] > data[1][i,3]:  # Home Win
                    simulation_matrix_regular[i,:] = np.matrix(np.zeros(simulations))
                if data[1][i,2] == data[1][i,3]:  # Tie
                    simulation_matrix_regular[i,:] = np.matrix(np.ones(simulations))
                if data[1][i,2] < data[1][i,3]:  # Away Win
                    simulation_matrix_regular[i,:] = np.matrix(2*np.ones(simulations))
            else:
                simulation_matrix_regular[i,:] = simulation_matrix[i,:]

    # Generate Output based on Monte Carlo Simulation
    # Determine number of points & league position for every team in every simulation

    sim_start = time.time()
    # points is matrix of size number_of_teams x simulation
    # unsorted (teams alphabetically) points for every team in every season
    points = np.zeros((number_of_teams, simulations))
    wins = np.zeros((number_of_teams, simulations))

    # league_ranking is matrix of size number_of_teams x simulation
    # sorted (descending) index of team on that position
    league_ranking = np.zeros((number_of_teams, simulations))
    league_ranking_distribution_po = list()
    for i in range(simulations):
        sim_start_lr = time.time()
        league_ranking_distribution_po.append(np.zeros((number_of_teams, number_of_teams)))
        for j in range(total_games):
            for k in range(number_of_teams):
                if data[1][j, 0] == k:  # Home Team
                    if simulation_matrix_regular[j, i] == 0:  # Home Team Victory
                        points[k, i] += 3
                        wins[k, i] += 1
                    if simulation_matrix_regular[j, i] == 1:  # Tie
                        points[k, i] += 1
                    if simulation_matrix_regular[j, i] == 2:  # Away Team Victory
                        points[k, i] += 0
                if data[1][j, 1] == k:  # Away team
                    if simulation_matrix_regular[j, i] == 0:  # Home Team Victory
                        points[k, i] += 0
                    if simulation_matrix_regular[j, i] == 1:  # Tie
                        points[k, i] += 1
                    if simulation_matrix_regular[j, i] == 2:  # Away Team Victory
                        points[k, i] += 3
                        wins[k, i] += 1

        # Make ranking for this simulation
        # 1. Sort by points
        league_ranking[:, i] = np.argsort(points[:, i])[::-1]  # Best Team index [0], Worst team index [15]

        # 2. If same amount of points, most wins
        for j in range(1,len(points)):
            if points[league_ranking[j,i],i] == points[league_ranking[j-1,i],i]:
                if wins[league_ranking[j,i],i] > wins[league_ranking[j-1,i],i]:
                    league_ranking[j,i],league_ranking[j-1,i] = league_ranking[j-1,i],league_ranking[j,i]

        # 3. Goal difference
        ################################################################################################################
        # Playoff 1
        ################################################################################################################
        po1_rank = list(range(6))
        po1_games = np.zeros((6*(6-1),data[1].shape[1]))
        simulation_matrix_po1 = np.zeros((6*(6-1),simulations_po))
        points_po1 = np.zeros((6, simulations_po))
        wins_po1 = np.zeros((6, simulations_po))
        count_game = 0
        for j in range(6):
            # Take points and wins from regular season
            # Points divided by 2 and ceiled (playoff 1 rules)
            points_po1[j,:] = np.ceil(points[league_ranking[j,i],i]/2) * np.ones((1, simulations_po))
            wins_po1[j,:] = wins[league_ranking[j,i],i] * np.ones((1, simulations_po))
            for l in range(6):
                if j is not l:
                    for k in range(len(data[1])):
                        if data[1][k,0] == league_ranking[j,i] and data[1][k,1] == league_ranking[l,i]:
                            po1_games[count_game,:] = data[1][k,:]
                            # No new monte carlo, too computationally expensive
                            simulation_matrix_po1[count_game,:] = simulation_matrix[k,0:simulations_po]
                            count_game += 1

        # league_ranking is matrix of size number_of_teams x simulation
        # sorted (descending) index of team on that position
        league_ranking_po1 = np.zeros((6, simulations_po))
        for sim in range(simulations_po):
            for j in range(len(po1_games)):
                for k in range(6):
                    if po1_games[j, 0] == league_ranking[po1_rank[k],i]:  # Home Team
                        if simulation_matrix_po1[j, sim] == 0:  # Home Team Victory
                            points_po1[k, sim] += 3
                            wins_po1[k, sim] += 1
                        if simulation_matrix_po1[j, sim] == 1:  # Tie
                            points_po1[k, sim] += 1
                        if simulation_matrix_po1[j, sim] == 2:  # Away Team Victory
                            points_po1[k, sim] += 0
                    if po1_games[j, 1] == league_ranking[po1_rank[k],i]:  # Away team
                        if simulation_matrix_po1[j, sim] == 0:  # Home Team Victory
                            points_po1[k, sim] += 0
                        if simulation_matrix_po1[j, sim] == 1:  # Tie
                            points_po1[k, sim] += 1
                        if simulation_matrix_po1[j, sim] == 2:  # Away Team Victory
                            points_po1[k, sim] += 3
                            wins_po1[k, sim] += 1

            # Make ranking for this simulation
            # 1. Sort by points
            league_ranking_po1[:, sim] = np.argsort(points_po1[:, sim])[::-1]  # Best Team index [0], Worst team index [15]

            # 2. If same amount of points, most wins
            for j in range(1,len(points_po1)):
                if points_po1[league_ranking_po1[j,sim],sim] == points[league_ranking_po1[j-1,sim],sim]:
                    if wins_po1[league_ranking_po1[j,sim],sim] > wins_po1[league_ranking_po1[j-1,sim],sim]:
                        league_ranking_po1[j,sim],league_ranking_po1[j-1,sim] = league_ranking_po1[j-1,sim],league_ranking_po1[j,sim]

            # 3. Remap to initial team number
            for j in range(6):
                league_ranking_po1[j, sim] = league_ranking[int(league_ranking_po1[j, sim]),i]

            # 4. League Ranking Distribution
            # league_ranking_distribution_elo = np.zeros((number_of_teams, number_of_teams))
            for j in range(6):
                # Some teams may not get simulated on every position
                # For example a very good team might never simulate in last place
                # For that reason we have to check this and extend array if necessary (with 0 values)
                possible_positions_j = np.unique(np.where(league_ranking_po1 == league_ranking[j,i])[0])
                amount_per_position_j = np.bincount(np.where(league_ranking_po1 == league_ranking[j,i])[0])
                # Remove zeros from amount_per_position_i
                amount_per_position_j = amount_per_position_j[amount_per_position_j != 0]
                for k in range(len(possible_positions_j)):
                    league_ranking_distribution_po[i][league_ranking[j,i], possible_positions_j[k]] = amount_per_position_j[k]
    
        ####################################################################################################################
        # Playoff 2
        ####################################################################################################################
        # League positions determine playoff 2 groep
        po2a_rank = [6,8,11,13] # Finished 7,9,12,14
        po2b_rank = [7,9,10,12]
        po2_rank = sorted(po2a_rank + po2b_rank)

        po2a_games = np.zeros((4*(4-1),data[1].shape[1]))
        po2b_games = np.zeros((4*(4-1),data[1].shape[1]))
        simulation_matrix_po2a = np.zeros((4*(4-1),simulations_po))
        simulation_matrix_po2b = np.zeros((4*(4-1),simulations_po))
        points_po2a = np.zeros((4, simulations_po)) # Start from 0
        points_po2b = np.zeros((4, simulations_po)) # Start from 0
        wins_po2a = np.zeros((4, simulations_po))
        wins_po2b = np.zeros((4, simulations_po))
        
        count_game = 0
        for j in po2a_rank:
            for l in po2a_rank:
                if j is not l:
                    for k in range(len(data[1])):
                        if data[1][k,0] == league_ranking[j,i] and data[1][k,1] == league_ranking[l,i]:
                            po2a_games[count_game,:] = data[1][k,:]
                            # No new monte carlo, too computationally expensive
                            simulation_matrix_po2a[count_game,:] = simulation_matrix[k,0:simulations_po]
                            count_game += 1
                            
        count_game = 0
        for j in po2b_rank:
            for l in po2b_rank:
                if j is not l:
                    for k in range(len(data[1])):
                        if data[1][k,0] == league_ranking[j,i] and data[1][k,1] == league_ranking[l,i]:
                            po2b_games[count_game,:] = data[1][k,:]
                            # No new monte carlo, too computationally expensive
                            simulation_matrix_po2b[count_game,:] = simulation_matrix[k,0:simulations_po]
                            count_game += 1

        # league_ranking is matrix of size number_of_teams x simulation
        # sorted (descending) index of team on that position
        league_ranking_po2a = np.zeros((4, simulations_po))
        league_ranking_po2b = np.zeros((4, simulations_po))
        league_ranking_po2 = np.zeros((8,simulations_po))
        for sim in range(simulations_po):
            for j in range(len(po2a_games)):
                for k in range(4):
                    if po2a_games[j, 0] == league_ranking[po2a_rank[k],i]:  # Home Team
                        if simulation_matrix_po2a[j, sim] == 0:  # Home Team Victory
                            points_po2a[k, sim] += 3
                            wins_po2a[k, sim] += 1
                        if simulation_matrix_po2a[j, sim] == 1:  # Tie
                            points_po2a[k, sim] += 1
                        if simulation_matrix_po2a[j, sim] == 2:  # Away Team Victory
                            points_po2a[k, sim] += 0
                    if po2a_games[j, 1] == league_ranking[po2a_rank[k],i]:  # Away team
                        if simulation_matrix_po2a[j, sim] == 0:  # Home Team Victory
                            points_po2a[k, sim] += 0
                        if simulation_matrix_po2a[j, sim] == 1:  # Tie
                            points_po2a[k, sim] += 1
                        if simulation_matrix_po2a[j, sim] == 2:  # Away Team Victory
                            points_po2a[k, sim] += 3
                            wins_po2a[k, sim] += 1

                    if po2b_games[j, 0] == league_ranking[po2b_rank[k],i]:  # Home Team
                        if simulation_matrix_po2b[j, sim] == 0:  # Home Team Victory
                            points_po2b[k, sim] += 3
                            wins_po2b[k, sim] += 1
                        if simulation_matrix_po2b[j, sim] == 1:  # Tie
                            points_po2b[k, sim] += 1
                        if simulation_matrix_po2b[j, sim] == 2:  # Away Team Victory
                            points_po2b[k, sim] += 0
                    if po2b_games[j, 1] == league_ranking[po2b_rank[k],i]:  # Away team
                        if simulation_matrix_po2b[j, sim] == 0:  # Home Team Victory
                            points_po2b[k, sim] += 0
                        if simulation_matrix_po2b[j, sim] == 1:  # Tie
                            points_po2b[k, sim] += 1
                        if simulation_matrix_po2b[j, sim] == 2:  # Away Team Victory
                            points_po2b[k, sim] += 3
                            wins_po2b[k, sim] += 1

            # Make ranking for this simulation
            # 1. Sort by points
            league_ranking_po2a[:, sim] = np.argsort(points_po2a[:, sim])[::-1]  # Best Team index [0], Worst team index [15]
            league_ranking_po2b[:, sim] = np.argsort(points_po2b[:, sim])[::-1]  # Best Team index [0], Worst team index [15]

            # 2. If same amount of points, most wins
            for j in range(1,len(points_po2a)):
                if points_po2a[league_ranking_po2a[j,sim],sim] == points[league_ranking_po2a[j-1,sim],sim]:
                    if wins_po2a[league_ranking_po2a[j,sim],sim] > wins_po2a[league_ranking_po2a[j-1,sim],sim]:
                        league_ranking_po2a[j,sim],league_ranking_po2a[j-1,sim] = league_ranking_po2a[j-1,sim],league_ranking_po2a[j,sim]
            for j in range(1,len(points_po2b)):
                if points_po2b[league_ranking_po2b[j,sim],sim] == points[league_ranking_po2b[j-1,sim],sim]:
                    if wins_po2b[league_ranking_po2b[j,sim],sim] > wins_po2b[league_ranking_po2b[j-1,sim],sim]:
                        league_ranking_po2b[j,sim],league_ranking_po2b[j-1,sim] = league_ranking_po2b[j-1,sim],league_ranking_po2b[j,sim]

            # 3. Remap to initial team number
            for j in range(4):
                league_ranking_po2a[j, sim] = league_ranking[po2a_rank[int(league_ranking_po2a[j, sim])],i]
                league_ranking_po2b[j, sim] = league_ranking[po2b_rank[int(league_ranking_po2b[j, sim])],i]

            # For now, make ranking of both groups in one: league_ranking_po2
            # TERRIBLE IMPLEMENTATION, IMPROVE
            count = 0
            for j in range(4):
                league_ranking_po2[count,sim] = league_ranking_po2a[j, sim]
                league_ranking_po2[count+1,sim] = league_ranking_po2b[j, sim]
                count += 2

            # 4. League Ranking Distribution
            # league_ranking_distribution_elo = np.zeros((number_of_teams, number_of_teams))
            for j in range(6,14):
                # Some teams may not get simulated on every position
                # For example a very good team might never simulate in last place
                # For that reason we have to check this and extend array if necessary (with 0 values)
                possible_positions_j = np.unique(np.where(league_ranking_po2 == league_ranking[j,i])[0])

                # Remap possible_positions_j tot league_ranking
                for k in range(len(possible_positions_j)):
                    possible_positions_j[k] = po2_rank[possible_positions_j[k]]

                amount_per_position_j = np.bincount(np.where(league_ranking_po2 == league_ranking[j,i])[0])
                # Remove zeros from amount_per_position_i
                amount_per_position_j = amount_per_position_j[amount_per_position_j != 0]
                for k in range(len(possible_positions_j)):
                    league_ranking_distribution_po[i][league_ranking[j,i], possible_positions_j[k]] = amount_per_position_j[k]

            # for j in range(4):
            #     # Some teams may not get simulated on every position
            #     # For example a very good team might never simulate in last place
            #     # For that reason we have to check this and extend array if necessary (with 0 values)
            #     possible_positions_j = np.unique(np.where(league_ranking_po2a == league_ranking[j,i])[0])
            #     amount_per_position_j = np.bincount(np.where(league_ranking_po2a == league_ranking[j,i])[0])
            #     # Remove zeros from amount_per_position_i
            #     amount_per_position_j = amount_per_position_j[amount_per_position_j != 0]
            #     for k in range(len(possible_positions_j)):
            #         league_ranking_distribution_po[i][league_ranking[j,i], possible_positions_j[k]] = amount_per_position_j[k]
            #
            # for j in range(4):
            #     # Some teams may not get simulated on every position
            #     # For example a very good team might never simulate in last place
            #     # For that reason we have to check this and extend array if necessary (with 0 values)
            #     possible_positions_j = np.unique(np.where(league_ranking_po2b == league_ranking[j,i])[0])
            #     amount_per_position_j = np.bincount(np.where(league_ranking_po2b == league_ranking[j,i])[0])
            #     # Remove zeros from amount_per_position_i
            #     amount_per_position_j = amount_per_position_j[amount_per_position_j != 0]
            #     for k in range(len(possible_positions_j)):
            #         league_ranking_distribution_po[i][league_ranking[j,i], possible_positions_j[k]] = amount_per_position_j[k]
                    
        ####################################################################################################################
        # Playoff 3
        ####################################################################################################################
        # League positions determine playoff 3 groep
        po3_rank = [14,15] # Finished 15, 16

        po3_games = np.zeros((5,data[1].shape[1]))
        simulation_matrix_po3 = np.zeros((5,simulations_po))
        points_po3 = np.zeros((2, simulations_po))
        points_po3[0,:] = 3*np.ones((1, simulations_po)) # Playoff 3 rule
        wins_po3 = np.zeros((2, simulations_po))

        count_game = 0
        for j in po3_rank:
            for l in po3_rank:
                if j is not l:
                    for k in range(len(data[1])):
                        if data[1][k,0] == league_ranking[j,i] and data[1][k,1] == league_ranking[l,i]:
                            po3_games[count_game,:] = data[1][k,:]
                            # No new monte carlo, too computationally expensive
                            simulation_matrix_po3[count_game,:] = simulation_matrix[k,0:simulations_po]
                            count_game += 1

        # Expand to 5 games
        po3_games[2,:] = po3_games[0,:]
        simulation_matrix_po3[2,:] = simulation_matrix_po3[0,:]
        po3_games[3,:] = po3_games[1,:]
        simulation_matrix_po3[3,:] = simulation_matrix_po3[1,:]
        po3_games[4,:] = po3_games[0,:]
        simulation_matrix_po3[4,:] = simulation_matrix_po3[0,:]
        # league_ranking is matrix of size number_of_teams x simulation
        # sorted (descending) index of team on that position
        league_ranking_po3 = np.zeros((2, simulations_po))
        for sim in range(simulations_po):
            for j in range(len(po3_games)):
                for k in range(2):
                    if po3_games[j, 0] == league_ranking[po3_rank[k],i]:  # Home Team
                        if simulation_matrix_po3[j, sim] == 0:  # Home Team Victory
                            points_po3[k, sim] += 3
                            wins_po3[k, sim] += 1
                        if simulation_matrix_po3[j, sim] == 1:  # Tie
                            points_po3[k, sim] += 1
                        if simulation_matrix_po3[j, sim] == 2:  # Away Team Victory
                            points_po3[k, sim] += 0
                    if po3_games[j, 1] == league_ranking[po3_rank[k],i]:  # Away team
                        if simulation_matrix_po3[j, sim] == 0:  # Home Team Victory
                            points_po3[k, sim] += 0
                        if simulation_matrix_po3[j, sim] == 1:  # Tie
                            points_po3[k, sim] += 1
                        if simulation_matrix_po3[j, sim] == 2:  # Away Team Victory
                            points_po3[k, sim] += 3
                            wins_po3[k, sim] += 1

            # Make ranking for this simulation
            # 1. Sort by points
            league_ranking_po3[:, sim] = np.argsort(points_po3[:, sim])[::-1]  # Best Team index [0], Worst team index [15]

            # 2. If same amount of points, most wins
            for j in range(1,len(points_po3)):
                if points_po3[league_ranking_po3[j,sim],sim] == points[league_ranking_po3[j-1,sim],sim]:
                    if wins_po3[league_ranking_po3[j,sim],sim] > wins_po3[league_ranking_po3[j-1,sim],sim]:
                        league_ranking_po3[j,sim],league_ranking_po3[j-1,sim] = league_ranking_po3[j-1,sim],league_ranking_po3[j,sim]

            # 3. Remap to initial team number
            for j in range(2):
                league_ranking_po3[j, sim] = league_ranking[po3_rank[int(league_ranking_po3[j, sim])],i]

            # 4. League Ranking Distribution
            # league_ranking_distribution_elo = np.zeros((number_of_teams, number_of_teams))
            for j in range(14,16):
                # Some teams may not get simulated on every position
                # For example a very good team might never simulate in last place
                # For that reason we have to check this and extend array if necessary (with 0 values)
                possible_positions_j = np.unique(np.where(league_ranking_po3 == league_ranking[j,i])[0])

                # Remap possible_positions_j tot league_ranking
                for k in range(len(possible_positions_j)):
                    possible_positions_j[k] = po3_rank[possible_positions_j[k]]

                amount_per_position_j = np.bincount(np.where(league_ranking_po3 == league_ranking[j,i])[0])
                # Remove zeros from amount_per_position_i
                amount_per_position_j = amount_per_position_j[amount_per_position_j != 0]
                for k in range(len(possible_positions_j)):
                    league_ranking_distribution_po[i][league_ranking[j,i], possible_positions_j[k]] = amount_per_position_j[k]

        sim_stop_lr = time.time()
        if i == 0:
            print('One LR iteration takes', round(sim_stop_lr - sim_start_lr,1), 'seconds')
            print('Total LR time is appr.', simulations*round(sim_stop_lr - sim_start_lr,1), 'seconds')


    league_ranking_distribution_po_final = np.zeros((number_of_teams,number_of_teams))
    for i in range(len(league_ranking_distribution_po)):
        league_ranking_distribution_po_final += league_ranking_distribution_po[i]
    league_ranking_distribution_po_final = league_ranking_distribution_po_final/(simulations_po*simulations_po)

    sim_end = time.time()
    print('Regular Season League Ranking Distribution finished in', round(sim_end - sim_start,0),'seconds')

    #
    # # Average amount of points for every team
    # # number_of_teams (ordered alphabetically) x 1 matrix
    # points_avg = np.sum(points, axis=1) / simulations

    # Percentage chance to end up in certain league position
    # number_of_teams (ordered alphabetically) x number_of_teams (ranking)
    league_ranking_distribution = np.zeros((number_of_teams, number_of_teams))
    # league_ranking_distribution_elo = np.zeros((number_of_teams, number_of_teams))
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
    league_ranking_distribution = np.around(league_ranking_distribution,5)

    return list([data[0],league_ranking_distribution,league_ranking_distribution_po_final])