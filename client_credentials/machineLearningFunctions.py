import numpy as np
import tensorflow as tf
import json
from sklearn.naive_bayes import GaussianNB

# Read in JSON file with song and their attributes
songs = json.load(open('songs.json'))
# Example printing the first song's danceability
print(songs[0]['body']['danceability'])

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

    print('cluster centers:', cluster_centers)


# Example
num_points = 100
dimensions = 10
points = np.random.uniform(0, 1000, [num_points, dimensions])
nClusters = 5
KMeansCluster(points, nClusters)



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
def predictSong(NBayes, predictionInput):
    # get predicted value
    predictedValue = NBayes.predict(predictionInput)
    print(predictedValue)
    return predictedValue

# Example
x = np.array([[-3, 7], [1, 5], [1, 2], [-2, 0], [2, 3], [-4, 0], [-1, 1], [1, 1], [-2, 2], [2, 7], [-4, 1], [-2, 7]])
y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])
model = getNBayes(x,y)
testValues = [[1,2],[3,4]]
predictSong(model, testValues)
