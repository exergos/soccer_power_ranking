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

# output[season][game] =    dict()
#                           output[season][game]["game_date"]
#                           output[season][game]["game_hour"]
#                           output[season][game]["host"]
#                           output[season][game]["visitor"]
#                           output[season][game]["result"]
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

########################################################################################################################
########################################################################################################################
def sporza(algorithm="update",number_of_seasons=1):
    if algorithm == "update":
        try:
            # Import previous file
            import pickle
            output = pickle.load(open("app_soccer_power_ranking/algorithms/data/sporza.p", "rb"))  # load from file sporza.p
        except FileNotFoundError:
            print("Can't find file to update. Select 'new' algorithm to make new file.")
        else:
            output = sporza_scrape(output, algorithm, number_of_seasons)
            output = sporza_extend_gd(output)
            output = sporza_extend_gm(output)
    else:
        if algorithm == "new":
            # Add if condition to make sure "new" algorithm is used at the start of a new season!
            output = sporza_scrape([], algorithm, number_of_seasons)
            output = sporza_extend_gd(output)
            output = sporza_extend_gm(output)

    # Save to file sporza.p
    import pickle
    pickle.dump(output, open("app_soccer_power_ranking/algorithms/data/sporza.p", "wb"))

    return output

# sporza_big gets ALL data from sporza website
def sporza_scrape(input_data, algorithm, number_of_seasons):
    print("Starting scrape of sporza.be")
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
    import copy
    output = copy.deepcopy(input_data)

    seasons_new = []
    if algorithm == "update":
        # Check seasons
        if number_of_seasons <= len(input_data): # Update only last season
            range_seasons = [0]
            seasons_new.append(seasons[0])
            print("Only last season will be updated")
        else: # Update last season & some previous seasons
            extra_seasons = number_of_seasons - len(input_data)
            range_seasons = [0]
            seasons_new.append(seasons[0])
            for i in range(extra_seasons):
                range_seasons.append(i+len(input_data))
                seasons_new.append(seasons[i+len(input_data)])
            print("Last season & " + str(extra_seasons) + " extra seasons will be updated")
    else:
        extra_seasons = number_of_seasons
        range_seasons = list(range(number_of_seasons))
        seasons_new = seasons[:number_of_seasons]

    # For season i
    count_seasons = 0
    for i in range_seasons: # range(1)
        if algorithm == "update":
            if i == 0:
                print("Updating last season")
            else:
                print("Updating extra season " + str(count_seasons) + " of " + str(extra_seasons))
        else:
            print("Scraping season " + str(count_seasons+1))
        # Only for 9 seasons (since 2006/2007) is goal minute data available//otherwise len(seasons) to get data from all seasons (no goal minutes)
        sim_start = time.time()

        # Open Season i Website
        season_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be' + seasons_new[count_seasons]['value']))

        # Games in Season i
        games = season_page.find_all("a", class_=["finished"])

        # Games still to play in Season i
        games_upcoming = season_page.find_all("a", class_=["upcoming"])

        games_upcoming_soup = []
        for j in range(len(games_upcoming)): # range(len(games))
            games_upcoming_soup.append(BeautifulSoup(urllib.request.urlopen('http://sporza.be' + games_upcoming[j]['href'])))

        # Check how many games are new and added to sporza.p
        new_upcoming_games = []

        if i == 0 and algorithm == "update": # Update latest season only
            # Check to see if there are doubles:
            del_elements_index = []
            for j in range(len(input_data[i])):
                for k in range(len(input_data[i])):
                    if j is not k:
                        if input_data[i][j]["game_date"] == input_data[i][k]["game_date"] and input_data[i][j]["host"] == input_data[i][k]["host"]:
                            if input_data[i][j]["played"] == "0":
                                del_elements_index.append(j)
                            if input_data[i][k]["played"] == "0":
                                del_elements_index.append(k)
            del_elements_index = list(set(del_elements_index))
            for j in del_elements_index:
                del output[i][j]
                del input_data[i][j]


            for j in range(len(games_upcoming_soup)): # range(len(games))
                game_date = games_upcoming_soup[j].find(id="metadata").get_text().replace('\n','').split(' ')[0]
                host = games_upcoming_soup[j].find_all("dt")[0].get_text().replace('\n','')

                match = 0
                for k in range(len(input_data[i])):
                    if input_data[i][k]["game_date"] == game_date and input_data[i][k]["host"] == host:
                        match = 1
                        continue
                if match == 0:
                        new_upcoming_games.append(j)
        else:
            new_upcoming_games = list(range(len(games_upcoming_soup)))

            # Append list for game j in season i
            output.append(list())

        count_upcoming_games = 0
        output_start_length = len(output[i])
        for j in new_upcoming_games:
            # Save all categories in dict
            if algorithm == "new":
                output_index = count_upcoming_games
            else:
                if i == 0:
                    output_index = output_start_length + count_upcoming_games
                else:
                    output_index = count_upcoming_games

            output[i].append(list())
            output[i][output_index] = dict()

            # Add data for new game
            # Game Date
            output[i][output_index]["game_date"] = games_upcoming_soup[j].find(id="metadata").get_text().replace('\n','').split(' ')[0]

            # Host
            output[i][output_index]["host"] = games_upcoming_soup[j].find_all("dt")[0].get_text().replace('\n','')

            # Visitor
            output[i][output_index]["visitor"] = games_upcoming_soup[j].find_all("dt")[1].get_text().replace('\n','')

            # Played?
            output[i][output_index]["played"] = "0"

            count_upcoming_games = count_upcoming_games + 1

        # Check how many games are new and added to sporza.p
        new_games = []
        
        # Get all soups of game pages
        games_soup = []
        for j in range(len(games)): # range(len(games))
            games_soup.append(BeautifulSoup(urllib.request.urlopen('http://sporza.be' + games[j]['href'])))

        if i == 0 and algorithm == "update": # Update latest season only
            for j in range(len(games_soup)): # range(len(games))
                game_date = games_soup[j].find(id="metadata").get_text().replace('\n','').split(' ')[0]
                host = games_soup[j].find_all("dt")[0].get_text().replace('\n','')

                match = 0
                for k in range(len(input_data[i])):
                    if input_data[i][k]["game_date"] == game_date and input_data[i][k]["host"] == host and input_data[i][k]["played"] == "1":
                        match = 1
                        continue
                    if input_data[i][k]["game_date"] == game_date and input_data[i][k]["host"] == host and input_data[i][k]["played"] == "0":
                        match = 0
                        # Remove upcoming game (to be replaced by finished game)
                        del output[i][k]
                        continue
                if match == 0:
                        new_games.append(j)
        else:
            new_games = list(range(len(games_soup)))

        #  For game j
        count_games = 0
        output_start_length = len(output[i])
        for j in new_games: # range(len(games))
            # Save all categories in dict
            if algorithm == "new":
                output_index = count_upcoming_games + count_games
            else:
                if i == 0:
                    output_index = output_start_length + count_upcoming_games + count_games
                else:
                    output_index = count_upcoming_games + count_games

            output[i].append(list())
            output[i][output_index] = dict()

            # Add data for new game
            # Game Date
            output[i][output_index]["game_date"] = games_soup[j].find(id="metadata").get_text().replace('\n','').split(' ')[0]

            # Game hour
            output[i][output_index]["game_hour"] = games_soup[j].find(id="metadata").get_text().replace('\n','').split(' ')[1]

            # Host
            output[i][output_index]["host"] = games_soup[j].find_all("dt")[0].get_text().replace('\n','')

            # Visitor
            output[i][output_index]["visitor"] = games_soup[j].find_all("dt")[1].get_text().replace('\n','')

            # Played?
            output[i][output_index]["played"] = "1"

            # Host goals
            output[i][output_index]["host_goal"] = games_soup[j].find_all("dd",class_=["score"])[0].get_text().replace('\n','')

            # Visitor goals
            output[i][output_index]["visitor_goal"] = games_soup[j].find_all("dd",class_=["score"])[1].get_text().replace('\n','')

            # Result
            if int(output[i][output_index]["host_goal"]) > int(output[i][output_index]["visitor_goal"]):
                output[i][output_index]["result"] = "1"
            else:
                if int(output[i][output_index]["host_goal"]) == int(output[i][output_index]["visitor_goal"]):
                    output[i][output_index]["result"] = "0"
                else:
                    output[i][output_index]["result"] = "-1"

            if len(games_soup[j].find_all(class_="GENERIC")) is not 0: # Forfait or Lack of data check
                # Referee
                output[i][output_index]["referee"] = games_soup[j].find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[1].replace('scheidsrechter: ','')

                # Stadium
                output[i][output_index]["stadium"] = games_soup[j].find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[2].replace('stadion: ','')

                # Spectators
                output[i][output_index]["spectators"] = games_soup[j].find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[4].replace('toeschouwers: ','')

                # Goal Data
                output[i][output_index]["host_goal_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "host goal")
                output[i][output_index]["visitor_goal_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "visitor goal")

                # Yellow Cards
                output[i][output_index]["host_yellow_card_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "host yellow_card")
                output[i][output_index]["visitor_yellow_card_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "visitor yellow_card")

                # Red Cards
                output[i][output_index]["host_red_card_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "host red_card")

                output[i][output_index]["visitor_red_card_data"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "visitor red_card")

                # Starting Team
                home_starting_team_dummy = games_soup[j].find_all(class_="GENERIC")[1].get_text().split('\n')[3].split(', ')
                home_starting_team_dummy[-1] = home_starting_team_dummy[-1][0:-1]
                output[i][output_index]["host_starting_team"] = '//'.join(home_starting_team_dummy)

                away_starting_team_dummy = games_soup[j].find_all(class_="GENERIC")[0].get_text().split('\n')[3].split(', ')
                away_starting_team_dummy[-1] = away_starting_team_dummy[-1][0:-1]
                output[i][output_index]["visitor_starting_team"] = '//'.join(away_starting_team_dummy)

                # Substitutions
                output[i][output_index]["host_substitution"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "host inout")
                output[i][output_index]["visitor_substitution"] = sporza_scrape_function(games_soup[j].find_all("ol",class_=["eventset1"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventsethalftime"])[0],
                                                           games_soup[j].find_all("ol",class_=["eventset2"])[0],
                                                           "visitor inout")

                # Managers
                output[i][output_index]["host_manager"] = games_soup[j].find(class_=["coach"]).get_text().replace('\n\xa0\n\n','').split('\n')[0]
                output[i][output_index]["visitor_manager"] = games_soup[j].find(class_=["coach"]).get_text().replace('\n\xa0\n\n','').split('\n')[1]
            else:
                # Just add empty string
                output[i][output_index]["referee"] = ''
                output[i][output_index]["stadium"] = ''
                output[i][output_index]["spectators"] = ''
                output[i][output_index]["host_goal_data"] = ''
                output[i][output_index]["visitor_goal_data"] = ''
                output[i][output_index]["host_yellow_card_data"] = ''
                output[i][output_index]["visitor_yellow_card_data"] = ''
                output[i][output_index]["host_red_card_data"] = ''
                output[i][output_index]["visitor_red_card_data"] = ''
                output[i][output_index]["host_starting_team"] = ''
                output[i][output_index]["visitor_starting_team"] = ''
                output[i][output_index]["host_substitution"] = ''
                output[i][output_index]["visitor_substitution"] = ''
                output[i][output_index]["host_manager"] = ''
                output[i][output_index]["visitor_manager"] = ''

            count_games = count_games + 1
        # Print amount of new games added
        print(str(count_games) + " new games added")

        sim_end = time.time()
        print('Season ' + str(count_seasons+1) + ' scraped in ' + str(round(sim_end - sim_start,0)) + ' seconds')
        count_seasons = count_seasons + 1
        
    return output

# helper function for sporza_scrape()
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

# helper function for sporza()
# expands output with goal difference (gd) for every minute
def sporza_extend_gd(input_data):
    import numpy as np
    # Parameters to use during calculations
    minutes = 90

    # For every season i
    for i in range(len(input_data)):
        # For every game j
        for j in range(len(input_data[i])):
            if input_data[i][j]["played"] == "0":
                continue
            # Dummy array:
            game_minute_dummy = np.zeros((minutes,2))

            # Host goals
            host_goal_minutes = list()
            if input_data[i][j]["host_goal_data"] is not '':
                for k in range(len(input_data[i][j]["host_goal_data"].split('//'))):
                    # Split '+' is for extra time goals: everything past 45 or 90 minute is 45 and 90
                    host_goal_minutes.append(int(input_data[i][j]["host_goal_data"].split('//')[k].split("'")[0].split('+')[0]))

            # Visitor goals
            visitor_goal_minutes = list()
            if input_data[i][j]["visitor_goal_data"] is not '':
                for k in range(len(input_data[i][j]["visitor_goal_data"].split('//'))):
                    # Split '+' is for extra time goals: everything past 45 or 90 minute is 45 and 90
                    visitor_goal_minutes.append(int(input_data[i][j]["visitor_goal_data"].split('//')[k].split("'")[0].split('+')[0]))


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
                input_data[i][j]["minute_" + str(int(k+1))] = game_minute_dummy[k,0]

    return input_data

# helper function for sporza()
# calculates host/tie/visitor percentage data, and replaces these in data
# uses GameMinute (gm) algorithm
def sporza_extend_gm(input_data, goal_difference = 16):
    ######################
# What does it return?
######################

# output[goal_difference][game_result][minute] as a dict
# for example: What is the chance the host wins if host is behind 2 goals at the 30 minute mark?
# output['-2']['1']['30']

    # Parameters:
    # input_data = output from sporza() function (NOT "spi" or "elo")
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
    # goal_difference = max goal difference that is being taken into account (10 standard, i.e. -5 to +5)

    minutes = 90
    # Now use this to calculate probability of win/tie/loss for every game situation (minute/goal difference)
    # Create game_minute_chances
    # For every delta, at every minute and given the end result, count how many occurences
    game_minute_chances = dict()

    # For every possible goal difference
    for i in range(goal_difference+1):
        game_minute_chances[str(int(i-goal_difference/2))] = dict()
        # For every end result j (-1: visitor win; 0= tie; 1: home win)
        for j in range(3):
            game_minute_chances[str(int(i-goal_difference/2))][str(int(j-1))] = dict()
            for k in range(minutes):
                game_minute_chances[str(int(i-goal_difference/2))][str(int(j-1))]["minute_" + str(int(k+1))] = 0

    # Now loop through all games to fill game_minute_chances
    # For every season i
    for i in range(len(input_data)):
        # For every game j
        for j in range(len(input_data[i])):
            if input_data[i][j]["played"] == "0":
                continue
            # For every minute k
            for k in range(minutes):
                # Check to see if game minutes input_data available
                if input_data[i][j] is not []:
                    gd = str(int(input_data[i][j]["minute_" + str(int(k+1))]))
                    game_minute_chances[gd][input_data[i][j]["result"]]["minute_" + str(int(k+1))] = game_minute_chances[gd][input_data[i][j]["result"]]["minute_" + str(int(k+1))] + 1

    # Make percentage chances of all occurrences
    # For every goal difference
    for i in range(len(game_minute_chances)):
        # For every minute
        for j in range(minutes):
            occurrences = game_minute_chances[str(int(i-goal_difference/2))]['-1']["minute_" + str(int(j+1))] +\
                        game_minute_chances[str(int(i-goal_difference/2))]['0']["minute_" + str(int(j+1))] +\
                        game_minute_chances[str(int(i-goal_difference/2))]['1']["minute_" + str(int(j+1))]
            # For every outcome
            if occurrences is not 0:
                for k in range(3):
                    game_minute_chances[str(int(i-goal_difference/2))][str(int(k-1))]["minute_" + str(int(j+1))] = game_minute_chances[str(int(i-goal_difference/2))][str(int(k-1))]["minute_" + str(int(j+1))]/occurrences

    # Now add fields to input input_data
    # For every minute
    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            if input_data[i][j]["played"] == "0":
                continue
            for k in range(minutes):
                gd = str(int(input_data[i][j]["minute_" + str(int(k+1))]))
                input_data[i][j]["minute_" + str(int(k+1)) + "_host"] = game_minute_chances[gd]["1"]["minute_" + str(int(k+1))]
                input_data[i][j]["minute_" + str(int(k+1)) + "_tie"] = game_minute_chances[gd]["0"]["minute_" + str(int(k+1))]
                input_data[i][j]["minute_" + str(int(k+1)) + "_visitor"] = game_minute_chances[gd]["-1"]["minute_" + str(int(k+1))]
    return input_data