from django.shortcuts import render 
from lbcleaderboard.scripts.data import RawData


def display_leaderboard(request, client = RawData()):
    client.PullData()
    client.StyleData()
    client.DataToWeb()
    return render(request, "index.html")
