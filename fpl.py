import requests
import json
import pandas as pd
import sys

url = "https://fantasy.premierleague.com/drf/bootstrap-static"
response = requests.get(url)
blob = response.content
data = json.loads(blob)
results = data["elements"]
#print(type(data))

#helper function to retrive data within nested JSON
class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None
        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)
            if not val:
                break
        return val

def formatData():
    for i in range(0,len(results)):
        player_name = DictQuery(results[i]).get("web_name")
        form = DictQuery(results[i]).get("form")
        dreamteam_count = DictQuery(results[i]).get("dreamteam_count")
        now_cost = DictQuery(results[i]).get("now_cost")
        total_points = DictQuery(results[i]).get("total_points")
        markScore = total_points/now_cost
        playingPosition = DictQuery(results[i]).get("element_type")
        playerName.append(player_name)
        playerForm.append(form)
        dreamTeamCount.append(dreamteam_count)
        currentCost.append(now_cost)
        totalPoints.append(total_points)
        specialScore.append(markScore)
        playerPlayingPosition.append(playingPosition)
        #print(player_name, dreamteam_count,form,format(markScore, '.2f'),playingPosition)

#creates pandas dataframe with columns
df = pd.DataFrame()
playerName = []
playerForm = []
dreamTeamCount = []
currentCost = []
totalPoints = []
specialScore = []
playerPlayingPosition = []

formatData()

#store data in its corresponding columns
df["Player Name"] = playerName
df["Player Form"] = playerForm
df["No. of Dream Team Apps"] = dreamTeamCount
df["Current Player Price"] = currentCost
df["Total Points"] = totalPoints
df["Mark's Special Score"] = specialScore
df["Player Position"] = playerPlayingPosition

#save to csv
df.to_csv("fpl.csv")