__author__ = 'Exergos'
######################
# What does it return?
######################

# output[goal_difference][game_result][minute]
#   goal_difference:    index 0 == -goal_difference (away team in front by goal_difference goals)
#                       index goal_difference == 0 (game tied)
#                       index goal_difference*2 == +goal_difference (home team in front by goal_difference goals)

#   game_result:    index 0 == End result was Away Win
#                   index 1 == End result was Tie
#                   index 2 == End result was Home Win

#   minute: index 0 == minute 1
#           index 89 == minute 90

def GameMinute():
    # To read data back (from file):
    obj = open('goal_minutes_data.txt', 'r')
    import ast
    data = ast.literal_eval(obj.read())
    # [0][season][games]: list of the home goals (size number of goals)
    # [1][season][games]: list of the away goals (size number of goals)

    import numpy as np
    # Parameters to use during calculations
    seasons = len(data[0])
    number_of_games = list()
    for i in range(seasons):
        number_of_games.append(len(data[0][i]))
    minutes = 90

    # games_per_minute[seasons][games]: array of size(90,1) (for every minute, goal difference (+ home game in front, - away team in front)
    games_per_minute = list()
    for i in range(seasons):
        for j in range(number_of_games[i]):
            # Save in:
            games_per_minute.append(list())
            # Dummy array:
            game_minute_dummy = np.zeros((minutes,2))
            if data[0][i][j] == []: # Home team didn't score
                if data[1][i][j] == []: # Away team didn't score
                    games_per_minute[i].append(game_minute_dummy)
                else: # Away team did score
                    for k in range(len(data[1][i][j])):
                        game_minute_dummy[(data[1][i][j][k]-1):minutes,0] = game_minute_dummy[(data[1][i][j][k]-1):minutes,0] - 1
                    game_minute_dummy[:,1] = -1
                    games_per_minute[i].append(game_minute_dummy)
            else: # Home team did score
                if data[1][i][j] == []: # Away team didn't score
                    for k in range(len(data[0][i][j])):
                        game_minute_dummy[(data[0][i][j][k]-1):minutes,0] = game_minute_dummy[(data[0][i][j][k]-1):minutes,0] + 1
                    game_minute_dummy[:,1] = 1
                    games_per_minute[i].append(game_minute_dummy)
                else: # Away team did score
                    for k in range(len(data[0][i][j])):
                        game_minute_dummy[(data[0][i][j][k]-1):minutes,0] = game_minute_dummy[(data[0][i][j][k]-1):minutes,0] + 1
                    for k in range(len(data[1][i][j])):
                        game_minute_dummy[(data[1][i][j][k]-1):minutes,0] = game_minute_dummy[(data[1][i][j][k]-1):minutes,0] - 1
                    if len(data[0][i][j]) > len(data[1][i][j]):
                        game_minute_dummy[:,1] = 1
                    else:
                        if len(data[0][i][j]) == len(data[1][i][j]):
                            game_minute_dummy[:,1] = 0
                        else:
                            game_minute_dummy[:,1] = -1
                    games_per_minute[i].append(game_minute_dummy)

    # Now use this to calculate probability of win/tie/loss for every game situation (minute/goal difference)
    # Output: list [Score Diff][End Result]: array of size(minutes,3) with % chance of Win/Tie/Loss
    # Goal difference: -5 (away winning) to +5 (home winning)
    goal_difference = 10
    goal_difference_list = list(range(-goal_difference,goal_difference + 1))
    output = [[] for x in range(len(goal_difference_list))]
    for i in range(len(goal_difference_list)):
        output[i] = [[] for x in range(3)] # Home Win/Tie/Away Win
        for j in range(len(output[i])):
            output[i][j] = [[0] for x in range(minutes)] # Home Win/Tie/Away Win

    for i in range(seasons):
        for j in range(number_of_games[i]):
            for k in range(minutes):
                # -20 == index 0, +20 == index 40
                index_goal_difference = int(games_per_minute[i][j][k,0]) + goal_difference
                # -1 (away win) == 0, 0 (tie) == 1, 1 (home win) == 2
                index_end_result = int(games_per_minute[i][j][k,1]) + 1
                output[index_goal_difference][index_end_result][k][0] = output[index_goal_difference][index_end_result][k][0] + 1

    # Make percentage chances of all occurences
    for i in range((goal_difference*2+1)):
        for j in range(minutes):
            # For game situation i and j, give all matches
            matches = output[i][0][j][0] + output[i][1][j][0] + output[i][2][j][0]
            print(matches)
            if matches == 0:
                for k in range(3):
                    output[i][k][j][0] = 0
            else:
                for k in range(3):
                    output[i][k][j][0] = output[i][k][j][0]/matches
    return output