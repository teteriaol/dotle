from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Heroes(models.Model):
    HeroID = models.IntegerField(default=0)
    CodeName = models.CharField(max_length=33, default="npc_dota_hero_base")
    Name = models.CharField(max_length=19, default="Hero")
    Role = models.CharField(max_length=60, default="Role")
    Rolelevels = models.CharField(max_length=16, default="1")
    Team = models.CharField(max_length=7, default="Radiant")
    AttackType = models.CharField(max_length=50, default="Melee")
    SimilarHeroesID = models.CharField(max_length=11, default="0,0,0")
    AttributePrimary = models.CharField(max_length=24, default="DOTA_ATTRIBUTE_ALL")
    LastHitChallengeRivalID = models.IntegerField(default=0)
    NameAliases = models.CharField(max_length=50, default="Hero")
    Adjectives = models.CharField(max_length=100, default="{}")

    def __str__(self):
        return self.Name


class DateHeroes(models.Model):
    Date = models.DateField()
    Hero = models.CharField(max_length=50)


class UserDates(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.ForeignKey(DateHeroes, on_delete=models.CASCADE)
    classic_isguessed = models.BooleanField()
    classic_attempts = models.IntegerField()
    ranked_isguessed = models.BooleanField()
    ranked_attempts = models.IntegerField()

class UserMMR(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mmr = models.IntegerField

class UserSeasons(models.Model):
    winner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    season_number = models.IntegerField()

