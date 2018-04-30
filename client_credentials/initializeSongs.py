# in => a string containing the name of the file 'songs.json' (initial playlist)
# out => a json file with added songs 'allSongs.json' (official songs and data)
import numpy as np
import pandas as pd
import json
import sys
from sklearn.naive_bayes import GaussianNB

def JSONtoVectorList(fileName):
    songs = json.load(open(fileName))
    songList = []
    for i in range(len(songs['body']['audio_features']
        )):
        attributeList = []
        attributeList.append(songs['body']['audio_features'][i]['danceability'])
        attributeList.append(songs['body']['audio_features'][i]['energy'])
        attributeList.append(songs['body']['audio_features'][i]['key'])
        attributeList.append(songs['body']['audio_features'][i]['loudness'])
        attributeList.append(songs['body']['audio_features'][i]['mode'])
        attributeList.append(songs['body']['audio_features'][i]['speechiness'])
        attributeList.append(songs['body']['audio_features'][i]['acousticness'])
        attributeList.append(songs['body']['audio_features'][i]['instrumentalness'])
        attributeList.append(songs['body']['audio_features'][i]['liveness'])
        attributeList.append(songs['body']['audio_features'][i]['valence'])
        attributeList.append(songs['body']['audio_features'][i]['tempo'])
        attributeList.append(songs['body']['audio_features'][i]['id'])
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
        data['songs'].append({'token':song[11],'attributes':data2,'classification':2})
 
    with open('allSongs.json', 'w') as file:
        json.dump(data, file)

songList = JSONtoVectorList('songs.json')
songsToJSON(songList)
print(json.load(open('allSongs.json')))
sys.stdout.flush()