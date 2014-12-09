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

# output[season][game]  [0]: Game Date
#                       [1]: Game Hour
#                       [2]: Referee
#                       [3]: Stadium
#                       [4]: Spectators
#                       [5]: Home Team
#                       [6]: Away Team
#                       [7]: Home Goals
#                       [8]: Away Goals
#                       [9]: Home goal scorers + minute
#                       [10]: Away goal scorers + minute
#                       [11]: Home yellow cards + minute
#                       [12]: Away yellow cards + minute
#                       [13]: Home red cards + minute
#                       [14]: Away red cards + minute
#                       [15]: Home starting team
#                       [16]: Away starting team
#                       [17]: Home substitutions
#                       [18]: Away substitutions

########################################################################################################################
########################################################################################################################

def sporza():
    # Time algorithm
    import time

    from bs4 import BeautifulSoup
    import urllib.request
    import numpy as np

    # Open Website & Scrape Data
    start_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be/cm/sporza/matchcenter/mc_voetbal/jupilerleague_1415'))

    # Seasons
    seasons = start_page.find_all("option")

    output = list()

    # For season i
    for i in range(0,9): # Only for 9 seasons (since 2006/2007) is goal minute data available//otherwise len(seasons) to get data from all seasons (no goal minutes)
        sim_start = time.time()

        output.append(list())
        season_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be' + seasons[i]['value']))
        games = season_page.find_all("a", class_=["finished"])

        # For game j
        for j in range(len(games)): # range(len(games))
            output[i].append(list())
            game_page = BeautifulSoup(urllib.request.urlopen('http://sporza.be' + games[j]['href']))
            # Get data from game
            # 1. Game Date
            output[i][j].append(game_page.find(id="metadata").get_text().replace('\n','').split(' ')[0])

            # 2. Game hour
            output[i][j].append(game_page.find(id="metadata").get_text().replace('\n','').split(' ')[1])

            if len(game_page.find_all(class_="GENERIC")) is not 0: # Forfait or Lack of data check
                # 3. Referee
                output[i][j].append(game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[1].replace('scheidsrechter: ',''))

                # 4. Stadium
                output[i][j].append(game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[2].replace('stadion: ',''))

                # 5. Spectators
                output[i][j].append(game_page.find_all("ul",class_=["lineupmetadata"])[0].get_text().split('\n')[4].replace('toeschouwers: ',''))
            else:
                # 3. Referee
                output[i][j].append('')

                # 4. Stadium
                output[i][j].append('')

                # 5. Spectators
                output[i][j].append('')

            # 6. Home Team
            output[i][j].append(game_page.find_all("dt")[0].get_text().replace('\n',''))

            # 7. Away Team
            output[i][j].append(game_page.find_all("dt")[1].get_text().replace('\n',''))

            # 8. Home goals
            output[i][j].append(game_page.find_all("dd",class_=["score"])[0].get_text().replace('\n',''))

            # 9. Away goals
            output[i][j].append(game_page.find_all("dd",class_=["score"])[1].get_text().replace('\n',''))

            if len(game_page.find_all(class_="GENERIC")) is not 0: # Forfait or Lack of data check

                # 10. Home goal scorers + minute (eventset1 == first half; eventset2 == second half)
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host goal"))

                # 11. Away goal scorers + minute (eventset1 == first half; eventset2 == second half)
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor goal"))
                # 12. Home yellow cards + minute
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host yellow_card"))
                # 13. Away yellow cards + minute
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor yellow_card"))
                # 14. Home red cards + minute
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host red_card"))
                # 15. Away red cards + minute
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor red_card"))
                # 16. Home starting team
                home_starting_team_dummy = game_page.find_all(class_="GENERIC")[0].get_text().split('\n')[3].split(', ')
                home_starting_team_dummy[-1] = home_starting_team_dummy[-1][0:-1]
                output[i][j].append(home_starting_team_dummy)

                # 17. Away starting team
                away_starting_team_dummy = game_page.find_all(class_="GENERIC")[1].get_text().split('\n')[3].split(', ')
                away_starting_team_dummy[-1] = away_starting_team_dummy[-1][0:-1]
                output[i][j].append(away_starting_team_dummy)

                # 18. Home substitutions (players in/out + minute)
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "host inout"))

                # 19. Away substitutions (players in/out + minute)
                output[i][j].append(sporza_scrape_function(game_page.find_all("ol",class_=["eventset1"])[0],
                                                           game_page.find_all("ol",class_=["eventsethalftime"])[0],
                                                           game_page.find_all("ol",class_=["eventset2"])[0],
                                                           "visitor inout"))
            else:
                # Just add empty string
                for i in range(10):
                    output[i][j].append('')

        sim_end = time.time()
        print('Season scraped in', sim_end - sim_start, 'seconds')
    return output

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
    return dummy_data_string

# To read data back:
# obj = open('goal_minutes_data.txt', 'r')
# import ast
# ast.literal_eval(obj.read())

