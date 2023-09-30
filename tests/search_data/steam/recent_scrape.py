import requests
from bs4 import BeautifulSoup

def recent_games(url):
    request  = requests.get(url)# enter steam url
    soup = BeautifulSoup(request.content)

    games = (soup.find_all("div", {"class": "game_name"}))

    recent_games_list = []

    for game in games:
        recent_games_list.append(game.text)

    return recent_games_list