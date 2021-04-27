import requests
from objects.result_obj import Result
from threading import Thread
import utilities.request_utils as requtils
import time
import math
import json


with open("hypixel_api_keys.txt") as keys_file:
    keys = keys_file.read().split()
    api_key = keys[0]
    if len(keys) > 1:
        other_keys = keys[1:]

with open("data/hypixel_game_names.json") as file:
    game_mapper_data = json.load(file)

def returnName(uuid, doReturn=True, resultObj=None):
    ign = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()[-1]["name"]
    if doReturn:
        return ign
    else:
        resultObj.result = ign

def returnUUID(name, doReturn=True, resultObj=None):
    player_data = requests.get("https://api.mojang.com/users/profiles/minecraft/" + name).json()
    if doReturn:
        return player_data["id"]
    else:
        resultObj.result = player_data["id"]

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

def map_game_id_to_name(session_dict):
    single_types = ["LIMBO", "MAIN", "REPLAY", "TOURNAMENT", "HOUSING", "WALLS3", "SURVIVAL_GAMES", "MCGO",
                    "BATTLEGROUND", "SPEED_UHC", "SUPER_SMASH", "PIT", ]

    classic_games = []

    ignore_name = ["LEGACY", "ARCADE", "PROTOTYPE", "DUELS"]
    dont_ignore_name = ["SKYBLOCK"]

    if session_dict["gameType"] in single_types:
        for x in game_mapper_data:
            if x["key"] == session_dict["gameType"]:
                return x["name"]
    elif session_dict["gameType"] in ignore_name:
        if session_dict["mode"] == "LOBBY":
            for x in game_mapper_data:
                if x["key"] == session_dict["gameType"]:
                    return x["name"]+" Lobby"
        else:
            for x in game_mapper_data:
                if x["key"] == session_dict["gameType"]:
                    for y in x["modes"]:
                        if y["key"] == session_dict["mode"]:
                            return y["name"]
    elif session_dict["gameType"] in dont_ignore_name:
        if session_dict["mode"] == "LOBBY":
            for x in game_mapper_data:
                if x["key"] == session_dict["gameType"]:
                    return x["name"]+" Lobby"
        else:
            for x in game_mapper_data:
                if x["key"] == session_dict["gameType"]:
                    for y in x["modes"]:
                        if y["key"] == session_dict["mode"]:
                            return f"{x['name']} {y['name']}".replace("SkyBlock", "SB")


    return session_dict["gameType"]

def getOnlineStatus(uuid, simple=False, doReturn=True, resultObj=None):
    if simple == False:
        player_stats_result = Result()
        url = f"https://api.hypixel.net/player?key={other_keys[0]}&uuid={uuid}"
        player_stats_thread = Thread(target=requtils.make_request, args=(url, False, player_stats_result))
        player_stats_thread.start()
    online_result = Result()
    url = f"https://api.hypixel.net/status?key={other_keys[0]}&uuid={uuid}"
    online_thread = Thread(target=requtils.make_request(url, False, online_result))
    online_thread.start()

    player_stats_thread.join()
    online_thread.join()

    status_data = online_result.result["session"]
    player_data = player_stats_result.result["player"]

    if simple:
        if doReturn:
            return status_data
        else:
            resultObj.result = status_data
            return

    if not status_data["online"]:
        if doReturn:
            return ["Offline",]
        else:
            resultObj.result = ["Offline",]
            return

    game_name = map_game_id_to_name(status_data)

    lastLogin = player_data["lastLogin"]/1000
    secondsOnline = time.time() - lastLogin

    hours = math.floor(secondsOnline / 3600)
    mins = math.floor((secondsOnline % 3600) / 60)
    secs = math.floor(secondsOnline % 60)

    ign = player_data["displayname"]

    if doReturn:
        return [f"Online", game_name, f"{hours}h {mins}m {secs}s", ign]
    else:
        resultObj.result = [f"Online", game_name, f"{hours}h {mins}m {secs}s", ign]

def check(contents):

    qsMin = requtils.make_request(f"https://api.hypixel.net/key?key="+other_keys[0])["record"]["queriesInPastMin"]
    if qsMin >= 70:
        return False

    threads = []
    result_objs = []
    for i, uuid in enumerate(contents):
        result_objs.append(Result())
        threads.append(Thread(target=getOnlineStatus, args=(uuid, False, False, result_objs[i])))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    output_list = []

    for result in result_objs:
        if result.result[0] == "Online":
            output_list.append([result.result[3], result.result[1], result.result[2]])

    return output_list