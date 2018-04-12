import numpy as np
import tensorflow as tf
import pandas as pd
import json
from sklearn.naive_bayes import GaussianNB

# Read in JSON file with song and their attributes
#songs = json.load(open('songs.json'))
# Example printing the first song's danceability
#print(songs[0])

# K-Means Clustering function for clustering songs based on attributes
# vectors is a list of lists of song attributes
# num_clusters is the number of desired clusters
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

# Example
#num_points = 100
#dimensions = 10
#points = np.random.uniform(0, 1000, [num_points, dimensions])
#nClusters = 5
#KMeansCluster(points, nClusters)

# put in a list of all of new songs and to classify them as unsure
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


# vectors is a list of lists of attributes of each song
# classification is a list of values corresponding to each list in X
# the value states song is liked, disliked, or neither
def getNBayes(vecotrs, classification):
    # Create a Gaussian Classifier
    model = GaussianNB()
    # Train the model using the training sets
    model.fit(vecotrs, classification)
    return model


# gets a predicted value based on a given NBayes model
def predictSongs(NBayes, predictionInput):
    # get predicted value
    predictedValue = NBayes.predict(predictionInput)
    print(predictedValue)
    return predictedValue


# gets rid of repeat songs
def consolidateSongLists(list1, list2):
    consolidatedList = []
    for i in range(len(list1)):

        for j in range(len(list2)):
            if list1[i] == list2[j]:
                consolidatedList
            else:
                consolidatedList.append(list1[i])
    return consolidatedList

    
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

# consolidate the predicted classification of spotify's reccomendations
# for each cluster of data into the three classification lists 
def getReccomendationLists(songs, model):
    # create lists of potential songs seperated by priority
    unlikedList = []
    likedList = []
    unsureList = []
    skippedList = []
    alreadyPlayed = []

    for i in range(len(songs)):
        #songs = getSpotifySeeds(clusters[i])

        # mock list of returned potential songs
        #songs = [clusters[i]]
        #songPredictions = predictSongs(model, songs)
        for j in range(len(songs[i])):
            if songPredictions[j] == 0:
                unlikedList.append(songPredictions[j])
            elif songPredictions[j] == 1:
                likedList.append(songPredictions[j])
            elif songPredictions[j] == 2:
                unsureList.append(songPredictions[j])
            else:
                skippedList.append(songPredictions[j])

    return (unlikedList, likedList, unsureList, skippedList)

# Example
songList = JSONtoVectorList('songs.json')
# only run once to get initial songs classified
songClassifications = initializePlaylistSongs(songList)
print("Song Classifications")
#print(songClassifications)
#print(songs)

# cluster the songs 
num_clusters = 6
clusters = KMeansCluster(songList, num_clusters)

print('Cluster Centers:')
cluster_centers = json.load(open('clusters.json'))
for i in range(len(clusters)):
    print(cluster_centers['cluster'][i])
    print()

# create a new model based off these songs
model = getNBayes(songList, songClassifications)
"""
# display the reccomended songs
tup = getReccomendationLists(clusters, model)
print(len(tup[0])," UNLIKED SONGS")
print(tup[0])
print(len(tup[1])," LIKED SONGS")
print(tup[1])
print(len(tup[2])," POTENTIAL SONGS")
print(tup[2])
print(len(tup[3])," SKIPPED SONGS")
print(tup[3])
"""

# pick a random song from the highest priority classification list and play that song
#alreadyPlayed.append(likedList.pop(0))
#alreadyPlayedCount +=1

# add all new song to the list of music
#tempList = likedList+unlikedList+skippedList+unsureList
#temp = consolidateSongLists(unlikedList, songDataTuple[0], 0)
#temp = consolidateSongLists(likeList, songDataTuple[0], 1)
#temp = consolidateSongLists(skippedList, songDataTuple[0], 2)
#temp = consolidateSongLists(unsureList, songDataTuple[0], 3)

# re-fit the data based on new input
#model = getNBayes(allSongData[0], classifications)




