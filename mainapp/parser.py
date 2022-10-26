import requests
from bs4 import BeautifulSoup
from .models import Player


url = 'https://www.rotowire.com/football/article/2022-ppr-fantasy-football-rankings-top-150-rotowire-64378'
response = requests.get(url)

list_names = []


def get_names():
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('ol').find_all('li')
    for name in quotes:
        a = name.getText()
        list_names.append(a.split(','))


get_names()

for player in list_names:
    player_bd = Player.objects.bulk_create([
        Player(name=player[0], position=player[1], team=player[2])
    ])
