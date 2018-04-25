# in => a string containing the name of the file 'songs.json' (initial playlist)
# out => a json file with added songs 'allSongs.json' (official songs and data)
import numpy as np
import tensorflow as tf
import pandas as pd
import json
from sklearn.naive_bayes import GaussianNB

def JSONtoVectorList(fileName):
    songs = json.load(open(fileName))
    songList = []
    for i in range(len(songs)):
        attributeList = []
        attributeList.append(songs[i]['body']['danceability'])
        attributeList.append(songs[i]['body']['energy'])
        attributeList.append(songs[i]['body']['key'])
        attributeList.append(songs[i]['body']['loudness'])
        attributeList.append(songs[i]['body']['mode'])
        attributeList.append(songs[i]['body']['speechiness'])
        attributeList.append(songs[i]['body']['acousticness'])
        attributeList.append(songs[i]['body']['instrumentalness'])
        attributeList.append(songs[i]['body']['liveness'])
        attributeList.append(songs[i]['body']['valence'])
        attributeList.append(songs[i]['body']['tempo'])
        attributeList.append(songs[i]['body']['id'])
        songList.append(attributeList)
    return songList

def songsToJSON(songs):
    data = {}
    data['songs'] = []
    
    for song in songs:
        data2 = {}
        data2['attributes'] = []
        song = np.array(song).tolist()
        #danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo
        data2 = {"danceability": song[0],"energy": song[1],"key": song[2],"loudness": song[3], 
        "mode": song[4],"speechiness": song[5],"acousticness": song[6],"instrumentalness": song[7],
        "liveness": song[8],"valence":song[9],"tempo":song[10]}
        data['songs'].append({'key':song[11],'attributes':data2,'classification':2})
 
    with open('allSongs.json', 'w') as file:
        json.dump(data, file)

songList = JSONtoVectorList('songs.json')
songsToJSON(songList)

