__author__ = 'Willem Lenaerts'
__project__ = 'SPI_JupilerProLeague'

########################################################################################################################
########################################################################################################################

#########################
# What does this file do?
#########################

# This file uses montecarlo.py to generate output and sends it to MySQL database automatically
# For now use local LAN server MySQL
# On MySQL server use following command:
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY PASSWORD 'some_characters' WITH GRANT OPTION

# And to connect, use LAN IP of server

# In the first connection a table was created with following command in python:
#

# Python 3.4 as Interpreter


# Some issues with trying to write rows of data to MySQL automatically (query issues)

########################################################################################################################
########################################################################################################################

# Generate output
import montecarlo
output = montecarlo.montecarlo(actual = 1)
# A list of 2 things
    # [0]:  List of 2 things
    # [0][0]: Team names of all teams in Jupiler Pro League
    # [0][1]: Array of size (number of teams x 3)
    #         [0][1][:,0]: SPI
    #         [0][1][:,1]: Off Rating
    #         [0][1][:,2]: Def Rating

    # [1]:  A size (number_of_teams x number_of_teams) matrix with the percentage chance of every team to end up in every
    #       possible league position


# Create table in database (via Transip)
import pymysql
conn = pymysql.connect(host='192.168.0.185', port=3306, user='root', passwd='Will0870', db='spi_index', charset='utf8', autocommit = True)

cur = conn.cursor()

# Remove old table
cur.execute("DROP TABLE IF EXISTS league_position")

# Create new table & first column (teams)
cur.execute("CREATE TABLE league_position ( Team varchar(255))")
column_names = "Team"
for i in range(len(output[1])):
     # Create new columns
     column_name = "place_" + str(i)
     column_names = column_names + ", " + column_name
     query = "ALTER TABLE league_position ADD (%s float(65,30))" % column_name
     cur.execute(query)

# Fill row by row
for i in range(len(output[0][0])):
    # Change numpy floats to python floats (sql connector only works this way)
    input_data_float = list()
    for j in range(len(output[1])):
        input_data_float.append(float(output[1][i,j]))

    input_data = (column_names,output[0][0][i]) + tuple(input_data_float)
    query = "INSERT INTO league_position (%s) VALUES " + "(" + (len(output[0][0]))*"%r, " + "%r)"
    query = query % input_data
    cur.execute(query)