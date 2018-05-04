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
        attributeList.append(float(songs['songs'][i]['attributes']['popularity']))
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
        attributeList.append(float(songs['songs'][i]['attributes']['popularity']))
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
    #print(reccomendationLists[0])
    #print(reccomendationLists[0][0]['attributes']['popularity'])
    
    #print(test)
    #print(reccomendationLists[0])
    for i in range(len(reccomendationLists)):
        sortedlist = sorted(reccomendationLists[i], key=lambda x: x['attributes']['popularity'], reverse=True)
        if len(sortedlist) > 10:
            j = random.randint(0,10)
            song = sortedlist[j]
            song['classification'] = i
            return song
        elif len(sortedlist) > 1:
            j = random.randint(0,len(sortedlist)-1)
            song = sortedlist[j]
            song['classification'] = i
            return song
        elif len(sortedlist) > 0:
            j = random.randint(0,len(sortedlist))
            song = sortedlist[0]
            song['classification'] = i
            return song

# classify all songs based on past songs
tup0 = JSONtoVectorList('pastSongs.json')
songList0 = tup0[0]
songTokenList0 = tup0[1]
songClassifications0 = tup0[2] 


tup1 = JSONtoVectorList('allSongs.json')
songList1 = tup1[0]
songTokenList1 = tup1[1]
songClassifications1 = tup1[2]

songs = json.load(open('allSongs.json'))
if len(songList0) > 0:
    model0 = getNBayes(songList0, songClassifications0)
    songPredictions = predictSongs(model0, songList1)
    #print(len(songs))
    print(songPredictions)
    for i in range(len(songs['songs'])):
        songs['songs'][i]['classification'] = int(songPredictions[i])
    with open('allSongs.json', 'w') as file:
        json.dump(songs, file)

# classify new songs based on all songs
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

print(song)
with open('nextSong.json', 'w') as file:
    json.dump(song, file)