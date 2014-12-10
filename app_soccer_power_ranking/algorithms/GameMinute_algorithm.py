__author__ = 'Exergos'
######################
# What does it return?
######################

# output[goal_difference][game_result][minute] as a dict
# for example: What is the chance the host wins if host is behind 2 goals at the 30 minute mark?
# output['-2']['1']['30']

def GameMinute(data, goal_difference = 16):
    # Parameters:
    # data = output from sporza() function (NOT "spi" or "elo")
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
    # Create output
    # For every delta, at every minute and given the end result, count how many occurences
    output = dict()

    # For every possible goal difference
    for i in range(goal_difference+1):
        output[str(int(i-goal_difference/2))] = dict()
        # For every end result j (-1: visitor win; 0= tie; 1: home win)
        for j in range(3):
            output[str(int(i-goal_difference/2))][str(int(j-1))] = dict()
            for k in range(minutes):
                output[str(int(i-goal_difference/2))][str(int(j-1))]["minute_" + str(int(k+1))] = 0

    # Now loop through all games to fill output
    # For every season i
    for i in range(len(data)):
        # For every game j
        for j in range(len(data[i])):
            # For every minute k
            for k in range(minutes):
                # Check to see if game minutes data available
                if data[i][j] is not []:
                    gd = str(int(data[i][j]["minute_" + str(int(k+1))]))
                    # Decide winner (+1: home team win; 0: tie;-1: away team win)
                    if int(data[i][j]["host_goal"]) > int(data[i][j]["visitor_goal"]):
                       gr = str(1)
                    else:
                        if int(data[i][j]["host_goal"]) == int(data[i][j]["visitor_goal"]):
                            gr = str(0)
                        else:
                            gr = str(-1)
                    output[gd][gr]["minute_" + str(int(k+1))] = output[gd][gr]["minute_" + str(int(k+1))] + 1

    # Make percentage chances of all occurrences
    # For every goal difference
    for i in range(len(output)):
        # For every minute
        for j in range(minutes):
            occurrences = output[str(int(i-goal_difference/2))]['-1']["minute_" + str(int(j+1))] +\
                        output[str(int(i-goal_difference/2))]['0']["minute_" + str(int(j+1))] +\
                        output[str(int(i-goal_difference/2))]['1']["minute_" + str(int(j+1))]
            # For every outcome
            if occurrences is not 0:
                for k in range(3):
                    output[str(int(i-goal_difference/2))][str(int(k-1))]["minute_" + str(int(j+1))] = output[str(int(i-goal_difference/2))][str(int(k-1))]["minute_" + str(int(j+1))]/occurrences

    return output