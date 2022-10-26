from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    team = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Лучшие игроки фентези'
        verbose_name_plural = 'Лучшие игроки фентези'
        ordering = ['id']


class ReviewRating(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    health = models.IntegerField()
    speed = models.IntegerField()
    body_strength = models.IntegerField()
    strength_environment = models.IntegerField()
    talent = models.IntegerField()
    created_on = models.DateField(auto_now=True)
    is_random_choice = models.BooleanField(default=False)

    def __str__(self):
        x = f'Player:{self.player} || User:{self.user}'
        return x

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосование'
        ordering = ['id']
