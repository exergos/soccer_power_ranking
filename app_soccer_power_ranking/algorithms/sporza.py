__author__ = 'Exergos'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This Scrape file gets Jupiler Pro League results data from sporza.be
# Python 3.4 as Interpreter
# BeautifulSoup to Scrape
# Numpy for Array use

######################
# What does it return?
######################

# Returns a list of 2 items
# [0]:  Team names of all teams in Jupiler Pro League
# [1]:  Array of size (games played x 4)
# [1][:,0]: Home Team (As a number, alphabetically as in [0]
#       [1][:,1]: Away Team (As a number, alphabetically as in [0]
#       [1][:,2]: Home Team Goals
#       [1][:,3]: Away Team Goals

########################################################################################################################
########################################################################################################################

def get_data():
    from bs4 import BeautifulSoup
    import urllib.request
    import numpy as np

    # Open Website & Scrape Data
    soup = []
    page_x = urllib.request.urlopen('http://sporza.be/cm/sporza/matchcenter/mc_voetbal/jupilerleague_1415')
    soup.append(BeautifulSoup(page_x))

    # Find all teams, home teams and scores for every game
    teams = []
    team_home = []
    team_away = []
    score_home = []
    score_away = []
    games_played = []

    scores_raw = soup[0].find_all("a", class_=["finished", "upcoming"])
    number_of_teams = 1
    for i in range(len(scores_raw)):
        if scores_raw[i]['class'][0] == "finished" and (
            '/' not in scores_raw[i].getText()):  # Second part is to eliminate postponed games
            games_played.append(i)
            team_home.append(scores_raw[i].parent.parent.find("abbr")["title"])
            score_home.append(float(scores_raw[i].getText().replace('\n', '').split('-')[0]))
            score_away.append(float(scores_raw[i].getText().replace('\n', '').split('-')[1]))
            if len(teams) == 0:  # First team added
                teams.append(scores_raw[i].parent.parent.find("abbr")["title"])
            else:
                if scores_raw[i].parent.parent.find("abbr")["title"] is not teams[number_of_teams - 1]:
                    teams.append(scores_raw[i].parent.parent.find("abbr")["title"])
                    number_of_teams = number_of_teams + 1

    # Find away teams
    team_away_dummy = []
    for i in range(number_of_teams):
        a = list(teams)
        a.pop(i)
        team_away_dummy.append(a)
    team_away_dummy = sum(team_away_dummy, [])  # Make one list from list of lists

    for i in range(len(games_played)):
        team_away.append(team_away_dummy[games_played[i]])

    # Change team_home and team_away from strings to numbers (based on ranking in teams list)
    # This is easier for future calculations
    for i in range(len(team_home)):
        for j in range(len(teams)):
            if team_home[i] == teams[j]:
                team_home[i] = j
            if team_away[i] == teams[j]:
                team_away[i] = j

    # Aggregate game data in one array
    game_data = np.zeros((len(team_home), 4))
    game_data[:, 0] = team_home
    game_data[:, 1] = team_away
    game_data[:, 2] = score_home
    game_data[:, 3] = score_away

    # What does module return?
    return list([teams, game_data])