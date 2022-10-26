from django.shortcuts import render

from NFLrating.celery import app
from mainapp.forms import ReviewForm
from mainapp.models import Player
import random


# @app.task
# def random_choice(request):
#     players = list(Player.objects.all())
#     random_players = random.sample(players, 3)
#
#     if request.method == 'POST':
#
#     else:
#         form = ReviewForm()
#         return render(request, "makechoice.html", {'form': form})
