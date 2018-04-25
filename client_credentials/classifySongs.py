# in => a string containing the name of the file 'reccomendedSongs.json' (a list of each clusters list of reccommended songs)
#       a json file with all official songs 'allSongs.json' (official songs and data)
# out => a json file 'nextSong.json' (A new song token) 
import numpy as np
import tensorflow as tf
import pandas as pd
import json
import sys
from sklearn.naive_bayes import GaussianNB

def JSONtoVectorList(fileName):
    songs = json.load(open(fileName))
    songList = []
    songTokenList = []
    songClassificationList = []
    for i in range(len(songs['songs'])):
        attributeList = []
        attributeList.append(float(songs['songs'][i]['attributes']['danceability']))
        attributeList.append(float(songs['songs'][i]['attributes']['energy']))
        attributeList.append(float(songs['songs'][i]['attributes']['key']))
        attributeList.append(float(songs['songs'][i]['attributes']['loudness']))
        attributeList.append(float(songs['songs'][i]['attributes']['mode']))
        attributeList.append(float(songs['songs'][i]['attributes']['speechiness']))
        attributeList.append(float(songs['songs'][i]['attributes']['acousticness']))
        attributeList.append(float(songs['songs'][i]['attributes']['instrumentalness']))
        attributeList.append(float(songs['songs'][i]['attributes']['liveness']))
        attributeList.append(float(songs['songs'][i]['attributes']['valence']))
        attributeList.append(float(songs['songs'][i]['attributes']['tempo']))
        songTokenList.append(songs['songs'][i]['key'])
        songClassificationList.append(songs['songs'][i]['classification'])
        songList.append(attributeList)
    return (songList, songTokenList, songClassificationList)

def getNBayes(vectors, classification):
    # Create a Gaussian Classifier
    model = GaussianNB()
    # Train the model using the training sets
    model.fit(vectors, classification)
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
        tup = JSONtoVectorList(clustersReccomendations)
        songList = tup[0]
        songTokenList = tup[1]
        songClassifications = tup[2] 
        songPredictions = predictSongs(model, songList)
        for j in range(len(songPredictions)):
            if songPredictions[j] == 0 and not unlikedList.__contains__(clustersReccomendations[j]):
                unlikedList.append(clustersReccomendations['songs'][j])
            elif songPredictions[j] == 1 and not likedList.__contains__(clustersReccomendations[j]):
                likedList.append(clustersReccomendations['songs'][j])
            elif songPredictions[j] == 2 and not unsureList.__contains__(clustersReccomendations[j]):
                unsureList.append(clustersReccomendations['songs'][j])
            elif songPredictions[j] == 3 and not skippedList.__contains__(clustersReccomendations[j]):
                skippedList.append(clustersReccomendations['songs'][j])

    return (likedList,unsureList,skippedList, unlikedList)

songsJson = 'allSongs.json'
tup = JSONtoVectorList(songsJson)
songList = tup[0]
songTokenList = tup[1]
songClassifications = tup[2] 
model = getNBayes(songList, songClassifications)

#songsJson = json.load(open('clusters.json'))
reccomendationLists = getReccomendationLists(songsJson, model)

song = []
if len(reccomendationLists[0]) > 0:
    song = reccomendationLists[0][0]
elif len(reccomendationLists[1])> 0:
    song = reccomendationLists[1][0]
elif len(reccomendationLists[2]) > 0:
    song = reccomendationLists[2][0]
else:
    song = reccomendationLists[3][0]
print(song)
 
with open('nextSong.json', 'w') as file:
    json.dump(song, file)

 
