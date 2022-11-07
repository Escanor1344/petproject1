from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    team = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Best fantasy players'
        verbose_name_plural = 'Best fantasy players'
        ordering = ['id']


class ReviewRating(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    speed = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    body_strength = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    strength_environment = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    talent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_on = models.DateField(auto_now=True)
    is_random_choice = models.BooleanField(default=False)

    def __str__(self):
        x = f'Player:{self.player} || User:{self.user}'
        return x

    class Meta:
        verbose_name = 'Voting'
        verbose_name_plural = 'Voting'
        ordering = ['id']
