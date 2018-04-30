# in => a string containing the name of the file 'allSongs.json' (official songs and data)
# out => a json file with clusters 'clusters.json' (cluster centers for reccommendation seeds)
import sys
import numpy as np
import tensorflow as tf
from sklearn.cluster import KMeans
import pandas as pd
import json
from sklearn.naive_bayes import GaussianNB

def JSONtoVectorList(fileName):
    songs = json.load(open(fileName))
    songList = []
    songTokenList = []
    songClassificationList = []
    for i in range(len(songs['songs'])):
        attributeList = []
        attributeList.append(songs['songs'][i]['attributes']['danceability'])
        attributeList.append(songs['songs'][i]['attributes']['energy'])
        attributeList.append(songs['songs'][i]['attributes']['key'])
        attributeList.append(songs['songs'][i]['attributes']['loudness'])
        attributeList.append(songs['songs'][i]['attributes']['mode'])
        attributeList.append(songs['songs'][i]['attributes']['speechiness'])
        attributeList.append(songs['songs'][i]['attributes']['acousticness'])
        attributeList.append(songs['songs'][i]['attributes']['instrumentalness'])
        attributeList.append(songs['songs'][i]['attributes']['liveness'])
        attributeList.append(songs['songs'][i]['attributes']['valence'])
        attributeList.append(songs['songs'][i]['attributes']['tempo'])
        songTokenList.append(songs['songs'][i]['token'])
        songClassificationList.append(songs['songs'][i]['classification'])
        songList.append(attributeList)
    return (songList, songTokenList, songClassificationList)

def clustersToJSON(clusters, tokens):
    data = {}
    data['cluster'] = []
    count = 0
    for cluster in clusters:
        cluster = np.array(cluster).tolist()
        #danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo
        data['cluster'].append({"limit":100,"seed_tracks":tokens[count],"danceability": cluster[0],"energy": cluster[1],"key": cluster[2],"loudness": cluster[3], 
        "mode": cluster[4],"speechiness": cluster[5],"acousticness": cluster[6],"instrumentalness": cluster[7],
        "liveness": cluster[8],"valence":cluster[9],"tempo":cluster[10]})
        count+=1
    
    with open('clusters.json', 'w') as file:
        json.dump(data, file)
        
def KMeansCluster(vectors, num_clusters, songTokenList):
    num_clusters = int(num_clusters)
    assert num_clusters < len(vectors)

    # Find out the dimensionality
    dim = len(vectors[0])
    
    kmeans = KMeans(n_clusters=num_clusters).fit(vectors)
    cluster_centers = kmeans.cluster_centers_

    tokens = []
    zero = []
    one = []
    two = []
    three = []
    four = []
    five = []

    count = 0
    for i in kmeans.labels_:
        if(i == 0 and len(zero) < 5):
            zero.append(songTokenList[count])
        if(i == 1 and len(one) < 5):
            one.append(songTokenList[count])
        if(i == 2 and len(two) < 5):
            two.append(songTokenList[count])
        if(i == 3 and len(three) < 5):
            three.append(songTokenList[count])
        if(i == 4 and len(four) < 5):
            four.append(songTokenList[count])
        if(i == 5 and len(five) < 5):
            five.append(songTokenList[count])
        count+=1

    tokens.append(zero)
    tokens.append(one)
    tokens.append(two)
    tokens.append(three)
    tokens.append(four)
    tokens.append(five)

    clustersToJSON(cluster_centers,tokens)
    return (cluster_centers, tokens)

# a string containing the name of the file 'songs.jason'
songsJson = 'allSongs.json' #sys.argv[1]

tup = JSONtoVectorList(songsJson)
songList = tup[0]
songTokenList = tup[1]
songClassifications = tup[2] 

# cluster the songs 
num_clusters = 6
clusters = KMeansCluster(songList, num_clusters, songTokenList)
cluster_centers = json.load(open('clusters.json'))
print(cluster_centers)