__author__ = 'Willem Lenaerts'
######################
# Input?
######################

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
#                           output[season][game]["minute_x with x from 1 tot 90
#                           output[season][game]["minute_x_host"] with x from 1 tot 90
#                           output[season][game]["minute_x_tie"] with x from 1 tot 90
#                           output[season][game]["minute_x_visitor"] with x from 1 tot 90

######################
# What does it return?
######################

# Returns a list of 2 items
# [0]:  List of 2 things
#       [0][0]: Team names of all teams in Jupiler Pro League

# [1]:  Array of size ((games played + games not played) x 8)
#       [1][:,0]: Home Team (As a number, alphabetically as in [0]
#       [1][:,1]: Away Team (As a number, alphabetically as in [0]
#       [1][:,2]: Home Team Goals
#       [1][:,3]: Away Team Goals
#       [1][:,4]: Game already played? (1 = yes, 0 = no)

def game_to_team(input_data):
    # Get some parameters
    games_played = len(input_data[0])

    # Only last season
    # Get team names
    team_names = []
    team_names.append([])
    for i in range(games_played):
        team_names[0].append(input_data[0][i]["host"])
    team_names[0] = sorted(set(team_names[0]))
    team_names.append([])
    team_names[1] = list(range(games_played))
    number_of_teams = len(team_names[0])

    # Get game_data
    import numpy as np
    game_data = np.zeros((games_played, 5))
    for i in range(games_played):
        for j in range(number_of_teams):
            if input_data[0][i]["host"] == team_names[0][j]:
                game_data[i,0] = team_names[1][j]
            if input_data[0][i]["visitor"] == team_names[0][j]:
                game_data[i,1] = team_names[1][j]
        game_data[i,2] = int(input_data[0][i]["host_goal"])
        game_data[i,3] = int(input_data[0][i]["visitor_goal"])
        game_data[i,4] = 1

    # Expand game_data to include games not played!
    # Extra rows for games not played, extra column(4) for information about game (1 = played, 0 = not played)
    # Define some parameters that will help with reading the code
    total_games = number_of_teams * (number_of_teams - 1)
    games_not_played = total_games - games_played

    game_data = np.r_[game_data, np.zeros((games_not_played, game_data.shape[1]))]
    count = 0
    for i in range(number_of_teams):  # Home Team
        for j in range(number_of_teams):  # Away Team
            played = 0
            if (i is not j):
                # Check to see if played
                for k in range(games_played):
                    if game_data[k, 0] == i and game_data[k, 1] == j:
                        played = 1
                        game_data[k, 4] = played
                if played == 0:
                    game_data[games_played + count, 0] = i
                    game_data[games_played + count, 1] = j
                    game_data[games_played + count, 4] = played
                    count = count + 1

    # What does module return?
    return list([team_names[0], game_data])
