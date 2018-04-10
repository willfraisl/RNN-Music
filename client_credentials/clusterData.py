import numpy as np
import tensorflow as tf

num_points = 100
dimensions = 10
points = np.random.uniform(0, 1000, [num_points, dimensions])
nClusters = 5

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

KMeansCluster(points, nClusters)

# Deep Learning is learns to classify potential Spotify songs as good
# or bad based the listeners interactions
def DeepLearning(vectors, num_clusters):
    print()
