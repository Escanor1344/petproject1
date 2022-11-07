from datetime import timedelta
from typing import Any
from django.db.models import Avg
from django.db.models import F
from mainapp.models import Player, ReviewRating


def in_four_days(user: object) -> dict[Any, timedelta | None | Any]:
    """ Checking if four days have passed since last voting for a player. """
    difference = {}
    for player in Player.objects.all():
        x = ReviewRating.objects.filter(user=user, player=player, is_random_choice=False).last()
        if x is not None:
            difference[player.id] = x.created_on + timedelta(4)
        else:
            difference[player.id] = None
    return difference


def in_seven_days(user: object) -> object:
    """ Checking if seven days have passed since last random voting. """
    any_record = ReviewRating.objects.filter(user=user, is_random_choice=True).exists()
    if any_record is True:
        last_random = ReviewRating.objects.filter(user_id=user, is_random_choice=True).last()
        seven_days = timedelta(7)
        difference = last_random.created_on + seven_days
        # Return date:
        # date = created date + 7 days
        return difference
    else:
        return None


def avg_rating() -> dict[Any, float | int]:
    """ Count average rating for all players on the page. """
    average = {}
    for player in Player.objects.all():
        total = ReviewRating.objects.filter(player=player).aggregate(
            avg=Avg((F('health') + F('speed') + F('body_strength') + F('strength_environment') + F('talent')) / 5.0)
        )
        if total.get('avg') is not None:
            average[player.id] = round(total.get('avg') * 2) / 2
        else:
            average[player.id] = 0
    return average
