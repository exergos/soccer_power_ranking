# This file will populate database
# Includes calculations for SPI (or refers to them)
# (see Tango with Django)

import os

def populate():
    # Remove previous data in table
    import django
    django.setup()
    spi_data.objects.all().delete()

    # SPI CALCULATION HERE
    # Algorithm to get data from sporza and calculate spi and league finish percentage chances
    # Located in map "algorithms" in app_soccer_power_ranking

    from app_soccer_power_ranking.algorithms.montecarlo import montecarlo
    output = montecarlo(actual = 1)
    # A list of 2 things
    # [0]:  List of 2 things
    # [0][0]: Team names of all teams in Jupiler Pro League
    # [0][1]: Array of size (number of teams x 3)
    #         [0][1][:,0]: SPI
    #         [0][1][:,1]: Off Rating
    #         [0][1][:,2]: Def Rating

    # [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
    #       possible league position

    # Fill Database
    # import numpy to work with arrays

    for i in range(len(output[0][0])): # For every team
        # this returns a dict with the property
        # name as key and the property val as its value

        # d is dictionary of field names and values
        d = {'Team' : output[0][0][i],'SPI' : output[0][1][i,0], 'off_rating' : output[0][1][i,1], 'def_rating' : output[0][1][i,2]}
        for j in range(16):
            d['finish_%s' % (j+1)] = output[1][i,j]

        spi_data.objects.create(**d)

# Start execution here!
if __name__ == '__main__':
    print("Starting SPI population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_soccer_power_ranking.settings')
    from app_soccer_power_ranking.models import spi_data
    populate()