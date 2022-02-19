import requests
import json
import random

def getmove(url):
    r = requests.get(url)
    try:
        data = r.json()
    except:
        return "error"
    total = int(data["white"])+int(data["draws"])+int(data["black"])
    mvs = len(data["moves"])
    if mvs <= 0:
        return "end"
    n = random.randrange(total)
    i = 0
    c = 0
    end = False
    while i < mvs and not end:
        c = c + int(data["moves"][i]["white"])
        c = c + int(data["moves"][i]["draws"])
        c = c + int(data["moves"][i]["black"])
        if c > n:
            end = True
        else:
            i = i + 1
    return data["moves"][i]["uci"]
