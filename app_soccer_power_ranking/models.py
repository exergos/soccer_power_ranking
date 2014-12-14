from django.db import models

# Create your models here.

class spi_data(models.Model):
    # Field 1: Team Name
    team = models.CharField(max_length=30)
    # Other fields: SPI, off rating, def rating
    spi = models.DecimalField(max_digits= 65, decimal_places= 2)
    off_rating = models.DecimalField(max_digits = 65, decimal_places = 2)
    def_rating = models.DecimalField(max_digits = 65, decimal_places = 2)

    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in spi_data._meta.fields]

# Other fields: possible league finishes (1 to 16)
for i in range(16):
    spi_data.add_to_class('finish_%s' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))

class elo_data(models.Model):
    # Field 1: Team Name
    team = models.CharField(max_length=30)
    # Other fields: SPI, off rating, def rating
    elo = models.DecimalField(max_digits= 65, decimal_places= 2)

    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in elo_data._meta.fields]

# Other fields: possible league finishes (1 to 16)
for i in range(16):
    elo_data.add_to_class('finish_%s' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))

class standings(models.Model):
    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in game_data._meta.fields]

    # Field 1: Team Name
    team = models.CharField(max_length=30)
    # Other fields: SPI, off rating, def rating
    games = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    tie = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in elo_data._meta.fields]

# Other fields: possible league finishes (1 to 16)
for i in range(16):
    elo_data.add_to_class('finish_%s' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))

class game_data(models.Model):
    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in game_data._meta.fields]

    # If sporza_big(number_of_seasons) is called:
    # output[season][game] =    dict()
    #                           output[season][game]["game_date"]
    #                           output[season][game]["game_hour"]
    #                           output[season][game]["host"]
    #                           output[season][game]["visitor"]
    #                           output[season][game]["played"]
    #                           output[season][game]["host_goal"]
    #                           output[season][game]["visitor_goal"]
    #                           output[season][game]["result"]
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
    game_date = models.TextField(default='')
    game_hour = models.TextField(default='')
    host = models.TextField(default='')
    visitor = models.TextField(default='')
    played = models.TextField(default='')
    host_goal = models.TextField(default='')
    visitor_goal = models.TextField(default='')
    result = models.TextField(default='')
    referee = models.TextField(default='')
    stadium = models.TextField(default='')
    spectators = models.TextField(default='')
    host_goal_data = models.TextField(default='')
    visitor_goal_data = models.TextField(default='')
    host_yellow_card_data = models.TextField(default='')
    visitor_yellow_card_data = models.TextField(default='')
    host_red_card_data = models.TextField(default='')
    visitor_red_card_data = models.TextField(default='')
    host_starting_team = models.TextField(default='')
    visitor_starting_team = models.TextField(default='')
    host_substitution = models.TextField(default='')
    visitor_substitution = models.TextField(default='')
    host_manager = models.TextField(default='')
    visitor_manager = models.TextField(default='')
    host_elo = models.DecimalField(max_digits= 65, decimal_places= 30)
    tie_elo = models.DecimalField(max_digits= 65, decimal_places= 30)
    visitor_elo = models.DecimalField(max_digits= 65, decimal_places= 30)
    host_spi = models.DecimalField(max_digits= 65, decimal_places= 30)
    tie_spi = models.DecimalField(max_digits= 65, decimal_places= 30)
    visitor_spi = models.DecimalField(max_digits= 65, decimal_places= 30)

# Other fields: All possible minutes
for i in range(90):
    game_data.add_to_class('minute_%s' % (i+1), models.IntegerField(default=0))
    game_data.add_to_class('minute_%s_host' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))
    game_data.add_to_class('minute_%s_tie' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))
    game_data.add_to_class('minute_%s_visitor' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))
