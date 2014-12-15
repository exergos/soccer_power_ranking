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

# [1]:  Array of size ((games played + games not played) x 5)
#       [1][:,0]: Home Team (As a number, alphabetically as in [0]
#       [1][:,1]: Away Team (As a number, alphabetically as in [0]
#       [1][:,2]: Home Team Goals
#       [1][:,3]: Away Team Goals
#       [1][:,4]: Game already played? (1 = yes, 0 = no)

def game_to_team(input_data):
    # Get some parameters
    games_played = []
    for i in range(len(input_data[0])):
        if input_data[0][i]["played"] == "1":
            games_played.append(i)
    total_games = len(input_data[0])

    # Only last season
    # Get team names
    team_names = []
    team_names.append([])
    for i in range(len(games_played)):
        # DIT IS PROBLEMATISCH BIJ NIEUW SEIZOEN, NOG NIET ELKE PLOEG HOST GEWEEST: OP TE LOSSEN
        team_names[0].append(input_data[0][games_played[i]]["host"])
    team_names[0] = sorted(set(team_names[0]))
    team_names.append([])
    team_names[1] = list(range(len(games_played)))
    number_of_teams = len(team_names[0])

    # Sort games based on date
    import time
    dates = []
    for i in range(total_games):
        dates.append(time.strptime(input_data[0][i]["game_date"],"%d/%m/%Y"))

    dates_sort_index = [i[0] for i in sorted(enumerate(dates), key=lambda x:x[1])]

    # Get game_data
    import numpy as np
    game_data = np.zeros((total_games, 5))
    count_games = 0
    for i in dates_sort_index:
        for j in range(number_of_teams):
            if input_data[0][i]["host"] == team_names[0][j]:
                game_data[count_games,0] = team_names[1][j]
            if input_data[0][i]["visitor"] == team_names[0][j]:
                game_data[count_games,1] = team_names[1][j]
        if input_data[0][i]["played"] == "1":
            game_data[count_games,2] = int(input_data[0][i]["host_goal"])
            game_data[count_games,3] = int(input_data[0][i]["visitor_goal"])
            game_data[count_games,4] = 1
        count_games = count_games + 1

    # Make ranking
    # Games Played - Wins - Losses - Ties - Goals For - Goals Against - Goal Diff - Points
    team_data = np.zeros((number_of_teams,8))
    for i in range(len(game_data)):
        if game_data[i,4] == 1: # Game played
            # Games played
            team_data[game_data[i,0],0] = team_data[game_data[i,0],0] + 1
            team_data[game_data[i,1],0] = team_data[game_data[i,1],0] + 1

            # Goals for and against Host
            team_data[game_data[i,0],4] = team_data[game_data[i,0],4] +  game_data[i,2]
            team_data[game_data[i,0],5] = team_data[game_data[i,0],5] +  game_data[i,3]

            # Goals for and against Visitor
            team_data[game_data[i,1],4] = team_data[game_data[i,1],4] +  game_data[i,3]
            team_data[game_data[i,1],5] = team_data[game_data[i,1],5] +  game_data[i,2]

            # Goal difference
            team_data[game_data[i,0],6] = team_data[game_data[i,0],6] + game_data[i,2] - game_data[i,3]
            team_data[game_data[i,1],6] = team_data[game_data[i,1],6] - game_data[i,2] + game_data[i,3]

            if game_data[i,2] > game_data[i,3]: # Host win
                # Points
                team_data[game_data[i,0],7] = team_data[game_data[i,0],7] + 3

                # Win Host
                team_data[game_data[i,0],1] = team_data[game_data[i,0],1] + 1

                # Loss Visitor
                team_data[game_data[i,1],2] = team_data[game_data[i,1],2] + 1
            else:
                if game_data[i,2] == game_data[i,3]: # Tie
                    # Points
                    team_data[game_data[i,0],7] = team_data[game_data[i,0],7] + 1
                    team_data[game_data[i,1],7] = team_data[game_data[i,1],7] + 1

                    # Tie Host
                    team_data[game_data[i,0],3] = team_data[game_data[i,0],3] + 1

                    # Tie Visitor
                    team_data[game_data[i,1],3] = team_data[game_data[i,1],3] + 1
                else: # Visitor Win
                    # Points
                    team_data[game_data[i,1],7] = team_data[game_data[i,1],7] + 3

                    # Loss Host
                    team_data[game_data[i,0],2] = team_data[game_data[i,0],2] + 1

                    # Win Visitor
                    team_data[game_data[i,1],1] = team_data[game_data[i,1],1] + 1

    # What does module return?
    return list([team_names[0], game_data, team_data])