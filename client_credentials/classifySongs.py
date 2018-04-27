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

def JSONtoVectorList2(fileName):
    #songs = json.load(open(fileName))
    songs = fileName
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
        songTokenList.append(songs['songs'][i]['token'])
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
    clustersReccomendations = json.load(open(clustersReccomendations))

    for i in range(len(clustersReccomendations['clusterRecommendations'])):
        clustersReccomendations = json.load(open('newSongs.json'))
        tup = JSONtoVectorList2(clustersReccomendations['clusterRecommendations'][i])
        songList = tup[0]
        songTokenList = tup[1]
        songClassifications = tup[2]
        songPredictions = predictSongs(model, songList)
        # condense all songs into respective lists, eliminating repeat songs
        for j in range(len(songPredictions)):
            if songPredictions[j] == 0 and not unlikedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                unlikedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
            elif songPredictions[j] == 1 and not likedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                likedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
            elif songPredictions[j] == 2 and not unsureList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                unsureList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
            elif songPredictions[j] == 3 and not skippedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                skippedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
    return (likedList,unsureList,skippedList, unlikedList)

tup = JSONtoVectorList('allSongs.json')
songList = tup[0]
songTokenList = tup[1]
songClassifications = tup[2] 
model = getNBayes(songList, songClassifications)
reccomendationLists = getReccomendationLists('newSongs.json', model)

song = []
if len(reccomendationLists[0]) > 0:
    songs = json.load(open('allSongs.json'))
    for i in range(len(reccomendationLists[0])):
        inList = False
        for j in range(len(songs['songs'])):
            if songs['songs'][j]['key'] == reccomendationLists[0][i]['token']:
                inList = True
        if not inList:
            song = reccomendationLists[0][i]
            break
        else:
            song = reccomendationLists[0][0]

elif len(reccomendationLists[1])> 0:
    songs = json.load(open('allSongs.json'))
    for i in range(len(reccomendationLists[1])):
        inList = False
        for j in range(len(songs['songs'])):
            if songs['songs'][j]['key'] == reccomendationLists[1][i]['token']:
                inList = True
        if not inList:
            song = reccomendationLists[1][i]
            break
        else:
            song = reccomendationLists[1][0]

elif len(reccomendationLists[2]) > 0:
    songs = json.load(open('allSongs.json'))
    for i in range(len(reccomendationLists[2])):
        inList = False
        for j in range(len(songs['songs'])):
            if songs['songs'][j]['key'] == reccomendationLists[3][i]['token']:
                inList = True
        if not inList:
            song = reccomendationLists[2][i]
            print(song)
            break
        else:
            song = reccomendationLists[2][0]

else:
    songs = json.load(open('allSongs.json'))
    for i in range(len(reccomendationLists[2])):
        inList = False
        for j in range(len(songs['songs'])):
            if songs['songs'][j]['key'] == reccomendationLists[3][i]['token']:
                inList = True
        if not inList:
            song = reccomendationLists[3][i]
            print(song)
            break
        else:
            song = reccomendationLists[3][0]

print(song)
with open('nextSong.json', 'w') as file:
    json.dump(song, file)