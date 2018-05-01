# in => a string containing the name of the file 'reccomendedSongs.json' (a list of each clusters list of reccommended songs)
#       a json file with all official songs 'allSongs.json' (official songs and data)
# out => a json file 'nextSong.json' (A new song token) 
import numpy as np
import tensorflow as tf
import pandas as pd
import json
import sys
import random
import webbrowser
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
        songTokenList.append(songs['songs'][i]['token'])
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
        songs = json.load(open('pastSongs.json'))
        for j in range(len(songPredictions)):
            inList = False
            for k in range(len(songs['songs'])):
                if songs['songs'][k]['token'] == clustersReccomendations['clusterRecommendations'][i]['songs'][j]['token']:
                    inList = True
                    break
            if(not inList):
                if songPredictions[j] == 3 and not unlikedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                    unlikedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
                elif songPredictions[j] == 0 and not likedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                    likedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
                elif songPredictions[j] == 1 and not unsureList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                    unsureList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
                elif songPredictions[j] == 2 and not skippedList.__contains__(clustersReccomendations['clusterRecommendations'][i]['songs'][j]):
                    skippedList.append(clustersReccomendations['clusterRecommendations'][i]['songs'][j])
            #else:
            #    print("repeat")
    return (likedList,unsureList,skippedList, unlikedList)

 # pick a song randomly from the top 10 or less songs
def getNextSong(reccomendationLists):
    for i in range(len(reccomendationLists)):
        if len(reccomendationLists[i]) > 10:
            j = random.randint(0,10)
            song = reccomendationLists[i][j]
            song['classification'] = i
            return song
        elif len(reccomendationLists[i]) > 1:
            j = random.randint(0,len(reccomendationLists[i]))
            song = reccomendationLists[i][j]
            song['classification'] = i
            return song
        elif len(reccomendationLists[i]) > 0:
            j = random.randint(0,len(reccomendationLists[i]))
            song = reccomendationLists[i][0]
            song['classification'] = i
            return song

tup = JSONtoVectorList('allSongs.json')
songList = tup[0]
songTokenList = tup[1]
songClassifications = tup[2] 
model = getNBayes(songList, songClassifications)
reccomendationLists = getReccomendationLists('newSongs.json', model)

song = []
song = getNextSong(reccomendationLists)

# play the preview if available
if song['previewURL'] != None:
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(song['previewURL'])

songs = json.load(open('newSongs.json'))
print(song)
with open('nextSong.json', 'w') as file:
    json.dump(song, file)