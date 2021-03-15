import requests
from objects.result_obj import Result
from threading import Thread


with open("hypixel_api_keys.txt") as keys_file:
    keys = keys_file.read().split()
    api_key = keys[0]
    if len(keys) > 1:
        other_keys = keys[1:]

def returnName(uuid):
    ign = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]
    return ign

def returnUUID(name):
    player_data = requests.get("https://api.mojang.com/users/profiles/minecraft/" + name).json()
    return player_data["id"]

# This is used in the !bwlb and !bwscore commands
def getUUIDBwStats(uuid, doReturn=True, result=None):
    data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()["player"]
    bw_data = data["stats"]["Bedwars"]
    ign = returnName(uuid)
    op = {
        "level": data["achievements"]["bedwars_level"],
        "wins": bw_data["wins_bedwars"],
        "losses": bw_data["losses_bedwars"],
        "final_kills": bw_data["final_kills_bedwars"],
        "final_deaths": bw_data["final_deaths_bedwars"],
        "kills": bw_data["kills_bedwars"],
        "deaths": bw_data["deaths_bedwars"],
        "beds_broken": bw_data["beds_broken_bedwars"],
        "beds_lost": bw_data["beds_lost_bedwars"]
    }
    if doReturn:
        return op
    else:
        result.result[ign] = op

def getIGNBwStats(ign):
    uuid = returnUUID(ign)
    data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()["player"]
    bw_data = data["stats"]["Bedwars"]
    op = {
        "level": data["achievements"]["bedwars_level"],
        "wins": bw_data["wins_bedwars"],
        "losses": bw_data["losses_bedwars"],
        "final_kills": bw_data["final_kills_bedwars"],
        "final_deaths": bw_data["final_deaths_bedwars"],
        "kills": bw_data["kills_bedwars"],
        "deaths": bw_data["deaths_bedwars"],
        "beds_broken": bw_data["beds_broken_bedwars"],
        "beds_lost": bw_data["beds_lost_bedwars"]
    }
    return op

def getAllPlayerBwStats(contents):

    stats_results = Result()
    threads = []

    for uuid in contents:
        threads.append(Thread(target=getUUIDBwStats, args=(uuid, False, stats_results)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    x = stats_results.result
    return x