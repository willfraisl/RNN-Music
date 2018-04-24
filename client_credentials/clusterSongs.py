# in => a string containing the name of the file 'songs.json'
# out => a json file with clusters 'clusters.json'
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
        songTokenList.append(songs[i]['body']['id'])
        songList.append(attributeList)
    return (songList, songTokenList)

def initializePlaylistSongs(songList):
    #vectors = []
    classification = []
    for i in range(len(songList)):
        #vectors.append(songList[i])
        classification.append(2)
    return classification

def clustersToJSON(clusters, tokens):
    data = {}
    data['cluster'] = []
    count = 0
    for cluster in clusters:
        print(tokens[count])
        cluster = np.array(cluster).tolist()
        #danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo
        data['cluster'].append({"seed_tracks":tokens[count],"danceability": cluster[0],"energy": cluster[1],"key": cluster[2],"loudness": cluster[3], 
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
songsJson = 'songs.json'#sys.argv[1]
tup = JSONtoVectorList(songsJson)
songList = tup[0]
songTokenList = tup[1]
# only run once to get initial songs classified
songClassifications = initializePlaylistSongs(songList)

# cluster the songs 
num_clusters = 6
clusters = KMeansCluster(songList, num_clusters, songTokenList)
cluster_centers = json.load(open('clusters.json'))
print(cluster_centers)