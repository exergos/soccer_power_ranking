from django.db import models

# Create your models here.

class spi_data(models.Model):
    # Field 1: Team Name
    Team = models.CharField(max_length=30)
    # Other fields: SPI, off rating, def rating
    SPI = models.DecimalField(max_digits= 65, decimal_places= 2)
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
    Team = models.CharField(max_length=30)
    # Other fields: SPI, off rating, def rating
    ELO = models.DecimalField(max_digits= 65, decimal_places= 2)

    # To loop through field names and field values in template
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in elo_data._meta.fields]

# Other fields: possible league finishes (1 to 16)
for i in range(16):
    elo_data.add_to_class('finish_%s' % (i+1), models.DecimalField(max_digits= 65, decimal_places= 30))

