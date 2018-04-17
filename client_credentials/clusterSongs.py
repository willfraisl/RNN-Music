# in => a string containing the name of the file 'songs.json'
# out => a json file with clusters 'clusters.json'
import sys
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
        songList.append(attributeList)
    return songList

def initializePlaylistSongs(songList):
    #vectors = []
    classification = []
    for i in range(len(songList)):
        #vectors.append(songList[i])
        classification.append(2)
    return classification

def clustersToJSON(clusters):
    data = {}
    data['cluster'] = []
    for cluster in clusters:
        cluster = np.array(cluster).tolist()
        #danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo
        data['cluster'].append({"danceability": cluster[0],"energy": cluster[1],"key": cluster[2],"loudness": cluster[3], 
        "mode": cluster[4],"speechiness": cluster[5],"acousticness": cluster[6],"instrumentalness": cluster[7],
        "liveness": cluster[8],"valence":cluster[9],"tempo":cluster[10]})

    with open('clusters.json', 'w') as file:
        json.dump(data, file)
        
def KMeansCluster(vectors, num_clusters):

    num_clusters = int(num_clusters)
    assert num_clusters < len(vectors)

    # Find out the dimensionality
    dim = len(vectors[0])

    def input_fn():
        return tf.train.limit_epochs(
            tf.convert_to_tensor(vectors, dtype=tf.float32), num_epochs=1)

    kmeans = tf.contrib.factorization.KMeansClustering(
        num_clusters=num_clusters, use_mini_batch=False)
    # train
    num_iterations = 10
    previous_centers = None
    for _ in range(num_iterations):
      kmeans.train(input_fn)
      cluster_centers = kmeans.cluster_centers()
      previous_centers = cluster_centers
    
    # convert the clusters to json format
    clustersToJSON(cluster_centers)
    
    return cluster_centers

# a string containing the name of the file 'songs.jason'
songsJson = sys.argv[1]

songList = JSONtoVectorList(songsJson)
# only run once to get initial songs classified
songClassifications = initializePlaylistSongs(songList)

# cluster the songs 
num_clusters = 6
clusters = KMeansCluster(songList, num_clusters)
cluster_centers = json.load(open('clusters.json'))
print(cluster_centers)