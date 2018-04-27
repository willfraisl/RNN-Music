import numpy as np
import tensorflow as tf
import pandas as pd
import json
import sys

def clustersToJSON(fileName):
    songs = json.load(open(fileName))
    data = {}
    data['clusterRecommendations'] = []
    count = 0
    for i in range(6):
        data2 = {}
        data2['songs'] = []
        for i in range(len(songs['body'])):
            #print(songs['body']['tracks'][i]['id'])
            #cluster = np.array(cluster).tolist()
            #danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo
            data2['songs'].append({"token":songs['body']['tracks'][i]['id'],"attributes": [], "classification": 2})
            count+=1
        data['clusterRecommendations'].append(data2)
    
    
    with open('newSongs.json', 'w') as file:

        json.dump(data, file)

clustersToJSON('reccomendedSongs.json')