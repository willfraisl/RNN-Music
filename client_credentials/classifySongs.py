# in => A JSON file with each clusters set of reccommended songs
# out => A new song token
import numpy as np
import tensorflow as tf
import pandas as pd
import json
import sys
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
    #print(predictedValue)
    return predictedValue

# in -> List of lists of songs reccommended from each cluster, 
#       Trained Naive Bayes prediction model
# out -> Tuple of lists of each classificantion of song
def getReccomendationLists(clustersReccomendations, model):
    # create lists of potential songs seperated by priority
    unlikedList = []
    likedList = []
    unsureList = []
    skippedList = []
    alreadyPlayed = []

    for i in range(len(clustersReccomendations)):
        songPredictions = predictSongs(model, clustersReccomendations[i])
        for j in range(len(songPredictions)):
            if songPredictions[j] == 0 and not unlikedList.__contains__(clustersReccomendations[i][j]):
                unlikedList.append(clustersReccomendations[i][j])
            elif songPredictions[j] == 1 and not likedList.__contains__(clustersReccomendations[i][j]):
                likedList.append(clustersReccomendations[i][j])
            elif songPredictions[j] == 2 and not unsureList.__contains__(clustersReccomendations[i][j]):
                unsureList.append(clustersReccomendations[i][j])
            elif songPredictions[j] == 3 and not skippedList.__contains__(clustersReccomendations[i][j]):
                skippedList.append(clustersReccomendations[i][j])

    return (unlikedList, likedList, unsureList, skippedList)

def initializePlaylistSongs(songList):
    #vectors = []
    classification = []
    for i in range(len(songList)):
        #vectors.append(songList[i])
        classification.append(2)
    return classification

songList = JSONtoVectorList('songs.json')
songClassifications = initializePlaylistSongs(songList)
model = getNBayes(songList, songClassifications)

songsJson = json.load(open('clusters.json'))
#print(songList)
reccomendationLists = getReccomendationLists(songList, model)
print(reccomendationLists[2])
 
