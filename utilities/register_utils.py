import requests

def isRegistered(ign):
    with open("data/registered_players.txt", "r") as player_file:
        contents = player_file.read().split()
    registered = False
    for uuid in contents:
        name = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]
        if name.lower() == ign.lower():
            registered = True
            return [True, name, uuid]
    return [False,]

def getRegistered(ign):
    with open("data/registered_players.txt", "r") as player_file:
        contents = player_file.read().split()
    return contents