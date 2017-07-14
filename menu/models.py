from django.db import models
import datetime

SEASON_CHOICES = (
    (1, 'Spring'),
    (2, 'Summer'),
    (3, 'Fall'),
    (4, 'Winter'),
)


class Menu(models.Model):
    season = models.SmallIntegerField(choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()
    items = models.ManyToManyField('Item', related_name='menus')
    created_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField()

    def __str__(self):
        return "{} {}".format(self.get_season_display(), self.year)


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    chef = models.ForeignKey('auth.User')
    created_date = models.DateField(default=datetime.date.today)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient',
                                         related_name='items')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
