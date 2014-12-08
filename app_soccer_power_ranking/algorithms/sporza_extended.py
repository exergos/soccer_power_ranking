__author__ = 'Exergos'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This Scrape file gets Jupiler Pro League results data from sporza.be
# Compared to "sporza.py" it gets data from all seasons, including goal minutes
# Python 3.3 as Interpreter
# BeautifulSoup to Scrape
# Numpy for Array use

######################
# What does it return?
######################

# Returns a list of 2 items
# [0]:  game_data, a list of size (seasons) that contains an array of size (number_of_games x 4) for every season
#       [0][season][:,0]: Home team
#       [0][season][:,1]: Away team
#       [0][season][:,2]: Goals Home Team
#       [0][season][:,3]: Goals Away Team

# [1]:  goals_scored, a list of size 2 (home and away) that each contains a list of size (seasons) that contains an array of size (number_of_games x 4) for every season
#       [1][0][season][games]: list of the home goals (size number of goals)
#       [1][1][season][games]: list of the away goals (size number of goals)


########################################################################################################################
########################################################################################################################

def sporza():
    # Time algorithm
    import time

    from bs4 import BeautifulSoup
    import urllib.request
    import numpy as np

    # Open Website & Scrape Data
    soup = []
    page_x = urllib.request.urlopen('http://sporza.be/cm/sporza/matchcenter/mc_voetbal/jupilerleague_1415')
    soup.append(BeautifulSoup(page_x))

    # Get
    seasons = soup[0].find_all("option")
    soup_link_season = list()
    link_season = list()

    teams = list()
    team_home = list()
    team_away = list()
    score_home = list()
    score_away = list()
    goal_minutes_home = list()
    goal_minutes_away = list()
    games_played = list()
    game_data = list()

    for i in range(0,9): # Only for 9 seasons (since 2006/2007) is goal minute data available//otherwise len(seasons) to get data from all seasons (no goal minutes)
        sim_start = time.time()
        # link_season to all the seasons
        link_season.append('http://sporza.be' + seasons[i]['value'])
        page_link_season = urllib.request.urlopen(link_season[i])
        soup_link_season.append([BeautifulSoup(page_link_season)])

        # Scrape results
        # Find all teams, home teams and scores for every game
        teams.append(list())
        team_home.append(list())
        team_away.append(list())
        score_home.append(list())
        score_away.append(list())
        games_played.append(list())

        scores_raw = soup_link_season[i][0].find_all("a", class_=["finished", "upcoming","in_play"])
        number_of_teams = 1

        for j in range(len(scores_raw)):
            if scores_raw[j]['class'][0] == "finished" and (
                        '/' not in scores_raw[j].getText()):  # Second part is to eliminate postponed games
                games_played[i].append(j)
                team_home[i].append(scores_raw[j].parent.parent.find("abbr")["title"])
                score_home[i].append(float(scores_raw[j].getText().replace('\n', '').split('-')[0]))
                score_away[i].append(float(scores_raw[j].getText().replace('\n', '').split('-')[1]))
                if len(teams[i]) == 0:  # First team added
                    teams[i].append(scores_raw[j].parent.parent.find("abbr")["title"])
                else:
                    if scores_raw[j].parent.parent.find("abbr")["title"] is not teams[i][number_of_teams - 1]:
                        teams[i].append(scores_raw[j].parent.parent.find("abbr")["title"])
                        number_of_teams = number_of_teams + 1

        # Find away teams
        team_away_dummy = []
        for j in range(number_of_teams):
            a = list(teams[i])
            a.pop(j)
            team_away_dummy.append(a)
        team_away_dummy = sum(team_away_dummy, [])  # Make one list from list of lists

        for j in range(len(games_played[i])):
            team_away[i].append(team_away_dummy[games_played[i][j]])

        # Change team_home and team_away from strings to numbers (based on ranking in teams list)
        # This is easier for future calculations
        for j in range(len(team_home[i])):
            for k in range(len(teams[i])):
                if team_home[i][j] == teams[i][k]:
                    team_home[i][j] = k
                if team_away[i][j] == teams[i][k]:
                    team_away[i][j] = k

        # Aggregate game data in one array
        game_data_dummy = np.zeros((len(team_home[i]), 4))
        game_data_dummy[:, 0] = team_home[i]
        game_data_dummy[:, 1] = team_away[i]
        game_data_dummy[:, 2] = score_home[i]
        game_data_dummy[:, 3] = score_away[i]

        game_data.append(list(game_data_dummy))

        # Scrape EVERY game of the selected season (i)
        soup_link_games = list()
        link_games = list()
        game_raw = soup_link_season[i][0].find_all("a", class_=["finished"])
        goals_season = list()
        goal_minutes_home.append(list())
        goal_minutes_away.append(list())
        for j in range(len(game_raw)):
            link_games.append('http://sporza.be' + game_raw[j]['href'])
            page_link_games = urllib.request.urlopen(link_games[j])
            soup_link_games.append(BeautifulSoup(page_link_games))
            goals_season.append(soup_link_games[j].find_all("dd", class_=["goals"]))

            goal_minutes_home[i].append([int(s) for s in goals_season[j][0].get_text().replace('\n',' ').replace("'","").replace('+','').split() if s.isdigit()])
            goal_minutes_away[i].append([int(s) for s in goals_season[j][1].get_text().replace('\n',' ').replace("'","").replace('+','').split() if s.isdigit()])

            # Fix extra time goals (replacing + by '' was step one)
            # set to 45min and 90 min
            for k in range(len(goal_minutes_home[i][j])):
                if len(str(goal_minutes_home[i][j][k])) == 3: # AFTER TIME GOAL
                    goal_minutes_home[i][j][k] = int(str(goal_minutes_home[i][j][k])[:2]) # + int(str(goal_minutes_home[i][j][k])[-1])  # Add this if you allow extra time goals (for instance: 93 minute)

            for k in range(len(goal_minutes_away[i][j])):
                if len(str(goal_minutes_away[i][j][k])) == 3: # AFTER TIME GOAL
                    goal_minutes_away[i][j][k] = int(str(goal_minutes_away[i][j][k])[:2]) # + int(str(goal_minutes_away[i][j][k])[-1])
        sim_end = time.time()
        print('Season scraped in', sim_end - sim_start, 'seconds')

    # To save data to file:
    obj = open('goal_minutes_data.txt', 'wb')
    obj.write(str([goal_minutes_home,goal_minutes_away]).encode('utf-8'))
    obj.close

    return [game_data ,[goal_minutes_home,goal_minutes_away]]



# To read data back:
# obj = open('goal_minutes_data.txt', 'r')
# import ast
# ast.literal_eval(obj.read())
