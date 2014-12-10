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
# If sporza_small() is called (algorithm="spi" or "elo"):
# Returns a list of 2 items
# [0]:  Team names of all teams in Jupiler Pro League
# [1]:  Array of size (total games x 4)
#       [1][:,0]: Home Team (As a number, alphabetically as in [0]
#       [1][:,1]: Away Team (As a number, alphabetically as in [0]
#       [1][:,2]: Home Team Goals
#       [1][:,3]: Away Team Goals
#       [1][:,4]: Game already played (1 = yes, 0 = no)

# If sporza_big(number_of_seasons) is called:
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
#                           output[season][game]["minute_x"] with x from 1 tot 90

########################################################################################################################
########################################################################################################################
def sporza(algorithm="GameMinute",number_of_seasons=1):
    if algorithm == "Ranking":
        output = sporza_small()

        # Save to file
        import pickle
        pickle.dump(output, open("app_soccer_power_ranking/algorithms/data/sporza_actual_season.p", "wb"))  # save it into a file named save.p
    else:
        output = sporza_big(number_of_seasons)
        output = sporza_game_minutes(output)
        # Save to file
        import pickle
        pickle.dump(output, open("app_soccer_power_ranking/algorithms/data/sporza_" + str(number_of_seasons) + "_seasons.p", "wb"))  # save it into a file named save.p
    return output

# sporza_big gets ALL data from sporza website
def sporza_big(number_of_seasons):
    # Time algorithm
    import time

    # Scraping tools
    from bs4 import BeautifulSoup
    import urllib.request

    # Open Main Website
    start_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be/cm/sporza/matchcenter/mc_voetbal/jupilerleague_1415'))

    # Seasons
    seasons = start_page.find_all("option")

    # All output will be stored in this list
    output = list()

    # For season i
    for i in range(number_of_seasons):
        # Only for 9 seasons (since 2006/2007) is goal minute data available//otherwise len(seasons) to get data from all seasons (no goal minutes)
        sim_start = time.time()

        # Append list for season i
        output.append(list())

        # Open Season i Website
        season_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be' + seasons[i]['value']))

        # Games in Season i
        games = season_page.find_all("a", class_=["finished"])

        # For game j
        for j in range(len(games)): # range(len(games))
            # Append list for game j in season i
            output[i].append(list())

            # Save all categories in dict
            output[i][j] = dict()

            # Open Game j Website
            game_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be' + games[j]['href']))

            # Get data from game
            # Game Date
            output[i][j]["game_date"] = game_page.find(id="metadata").get_text().replace('\n','').split(' ')[0]

            # Game hour
            output[i][j]["game_hour"] = game_page.find(id="metadata").get_text().replace('\n','').split(' ')[1]

            # Host
            output[i][j]["host"] = game_page.find_all("dt")[0].get_text().replace('\n','')

            # Visitor
            output[i][j]["visitor"] = game_page.find_all("dt")[1].get_text().replace('\n','')

            # Host goals
            output[i][j]["host_goal"] = game_page.find_all("dd",class_=["score"])[0].get_text().replace('\n','')

            # Visitor goals
            output[i][j]["visitor_goal"] = game_page.find_all("dd",class_=["score"])[1].get_text().replace('\n','')

            if len(game_page.find_all(class_="GENERIC")) is not 0: # Forfait or Lack of data check
                # Referee
                output[i][j]["referee"] = game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[1].replace('scheidsrechter: ','')

                # Stadium
                output[i][j]["stadium"] = game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[2].replace('stadion: ','')

                # Spectators
                output[i][j]["spectators"] = game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[4].replace('toeschouwers: ','')

                # Goal Data
                output[i][j]["host_goal_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host goal")
                output[i][j]["visitor_goal_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor goal")

                # Yellow Cards
                output[i][j]["host_yellow_card_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host yellow_card")
                output[i][j]["visitor_yellow_card_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor yellow_card")

                # Red Cards
                output[i][j]["host_red_card_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host red_card")

                output[i][j]["visitor_red_card_data"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor red_card")

                # Starting Team
                home_starting_team_dummy = game_page.find_all(class_="GENERIC")[1].get_text().split('\n')[3].split(', ')
                home_starting_team_dummy[-1] = home_starting_team_dummy[-1][0:-1]
                output[i][j]["host_starting_team"] = '//'.join(home_starting_team_dummy)

                away_starting_team_dummy = game_page.find_all(class_="GENERIC")[0].get_text().split('\n')[3].split(', ')
                away_starting_team_dummy[-1] = away_starting_team_dummy[-1][0:-1]
                output[i][j]["visitor_starting_team"] = '//'.join(away_starting_team_dummy)

                # Substitutions
                output[i][j]["host_substitution"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host inout")
                output[i][j]["visitor_substitution"] = sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor inout")

                # Managers
                output[i][j]["host_manager"] = game_page.find(class_=["coach"]).get_text().replace('\n\xa0\n\n','').split('\n')[0]
                output[i][j]["visitor_manager"] = game_page.find(class_=["coach"]).get_text().replace('\n\xa0\n\n','').split('\n')[1]
            else:
                # Just add empty string
                output[i][j]["referee"] = ''
                output[i][j]["stadium"] = ''
                output[i][j]["spectators"] = ''
                output[i][j]["host_goal_data"] = ''
                output[i][j]["visitor_goal_data"] = ''
                output[i][j]["host_yellow_card_data"] = ''
                output[i][j]["visitor_yellow_card_data"] = ''
                output[i][j]["host_red_card_data"] = ''
                output[i][j]["visitor_red_card_data"] = ''
                output[i][j]["host_starting_team"] = ''
                output[i][j]["visitor_starting_team"] = ''
                output[i][j]["host_substitution"] = ''
                output[i][j]["visitor_substitution"] = ''
                output[i][j]["host_manager"] = ''
                output[i][j]["visitor_manager"] = ''

        sim_end = time.time()
        print('Season scraped in', sim_end - sim_start, 'seconds')
    return output

# sporza_small gets only results, and only for one season
def sporza_small():
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

    scores_raw = soup[0].find_all("a", class_=["finished", "upcoming","in_play"])
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

    # Expand game_data to include games not played!
    # Extra rows for games not played, extra column(4) for information about game (1 = played, 0 = not played)
    # Define some parameters that will help with reading the code
    total_games = number_of_teams * (number_of_teams - 1)
    games_played = len(game_data)
    games_not_played = total_games - games_played

    game_data = np.r_[game_data, np.zeros((games_not_played, game_data.shape[1]))]
    game_data = np.c_[game_data, np.zeros((total_games, 1))]
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
    return list([teams, game_data])

# helper function for sporza_big
def sporza_scrape_function(first_half,halftime,second_half,info):
    # Take into account first and second yellow
    if info == "host yellow_card" or info == "visitor yellow_card":
        dummy_data = second_half.find_all(class_=info + "1") \
                     + second_half.find_all(class_=info + "2") \
                     + halftime.find_all(class_=info + "1") \
                     + halftime.find_all(class_=info + "2") \
                     + first_half.find_all(class_=info + "1") \
                     + first_half.find_all(class_=info + "2")
    else:
        # Take into account own goals
        if info == "host goal" or info == "visitor goal":
            dummy_data = second_half.find_all(class_=info.replace(" goal"," own_goal")) \
                         +second_half.find_all(class_=info.replace(" goal"," penalty_scored")) \
                         + second_half.find_all(class_=info) \
                         + halftime.find_all(class_=info.replace(" goal"," own_goal")) \
                         + halftime.find_all(class_=info.replace(" goal"," penalty_scored")) \
                         + halftime.find_all(class_=info) \
                         + first_half.find_all(class_=info.replace(" goal"," own_goal")) \
                         + first_half.find_all(class_=info.replace(" goal"," penalty_scored")) \
                         + first_half.find_all(class_=info)
        else:
            dummy_data = second_half.find_all(class_=info) \
                         + halftime.find_all(class_=info) \
                         + first_half.find_all(class_=info)


    dummy_data_string = ''
    for k in range(len(dummy_data)):
        if k == 0:
            dummy_data_string = dummy_data[k]['title']
        else:
            dummy_data_string = dummy_data_string + '//' + dummy_data[k]['title']
    dummy_data_string = dummy_data_string.replace('<br>','//') # For substitutions in same minute
    return dummy_data_string

# helper function for sporza big
# expands output with game minute data
def sporza_game_minutes(data):
    import numpy as np
    # Parameters to use during calculations
    minutes = 90

    # For every season i
    for i in range(len(data)):
        # For every game j
        for j in range(len(data[i])):
            # Dummy array:
            game_minute_dummy = np.zeros((minutes,2))

            # Host goals
            host_goal_minutes = list()
            if data[i][j]["host_goal_data"] is not '':
                for k in range(len(data[i][j]["host_goal_data"].split('//'))):
                    # Split '+' is for extra time goals: everything past 45 or 90 minute is 45 and 90
                    host_goal_minutes.append(int(data[i][j]["host_goal_data"].split('//')[k].split("'")[0].split('+')[0]))

            # Visitor goals
            visitor_goal_minutes = list()
            if data[i][j]["visitor_goal_data"] is not '':
                for k in range(len(data[i][j]["visitor_goal_data"].split('//'))):
                    # Split '+' is for extra time goals: everything past 45 or 90 minute is 45 and 90
                    visitor_goal_minutes.append(int(data[i][j]["visitor_goal_data"].split('//')[k].split("'")[0].split('+')[0]))


            if host_goal_minutes == []: # Home team didn't score
                # If away team didn't score, game_minute_dummy is correct
                if visitor_goal_minutes is not []: # Away team did score
                    for k in range(len(visitor_goal_minutes)):
                        game_minute_dummy[(visitor_goal_minutes[k]-1):minutes,0] = game_minute_dummy[(visitor_goal_minutes[k]-1):minutes,0] - 1
                    game_minute_dummy[:,1] = -1
            else: # Home team did score
                if visitor_goal_minutes == []: # Away team didn't score
                    for k in range(len(host_goal_minutes)):
                        game_minute_dummy[(host_goal_minutes[k]-1):minutes,0] = game_minute_dummy[(host_goal_minutes[k]-1):minutes,0] + 1
                    game_minute_dummy[:,1] = 1
                else: # Away team did score
                    for k in range(len(host_goal_minutes)):
                        game_minute_dummy[(host_goal_minutes[k]-1):minutes,0] = game_minute_dummy[(host_goal_minutes[k]-1):minutes,0] + 1
                    for k in range(len(visitor_goal_minutes)):
                        game_minute_dummy[(visitor_goal_minutes[k]-1):minutes,0] = game_minute_dummy[(visitor_goal_minutes[k]-1):minutes,0] - 1
                    if len(host_goal_minutes) > len(visitor_goal_minutes):
                        game_minute_dummy[:,1] = 1
                    else:
                        if len(host_goal_minutes) == len(visitor_goal_minutes):
                            game_minute_dummy[:,1] = 0
                        else:
                            game_minute_dummy[:,1] = -1

            # Define dict key for every minute
            for k in range(minutes):
                data[i][j]["minute_" + str(int(k+1))] = game_minute_dummy[k,0]
    return data

