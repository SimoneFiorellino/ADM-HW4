import numpy as np
import random

# how to use k_means:
# import k_means as km
# 
# my_k_means = km.k_means(my_data, num_centroids = 5, max_iterations = n)
# print(my_k_means.kmeans())

class k_means:
    
    def __init__(self, data, num_centroids, max_iterations = 3):
        self.iterations = 0
        self.data = data 
        self.max_iterations = max_iterations 
        

        self.num_centroids = num_centroids
        self.num_training_data = data.shape[0] # 
        self.num_features = data.shape[1]

        self.centroids = self.get_random_centroids()
        self.old_centroids = np.zeros(self.centroids.shape)

        self.labels = np.zeros(self.num_training_data)
        self.distances = np.zeros((self.num_training_data,self.num_centroids))

    def get_random_centroids(self):
        mean = np.mean(self.data, axis = 0)
        std = np.std(self.data, axis = 0)
        return np.random.randn(self.num_centroids,self.num_features)*std + mean

    def kmeans(self):
        while not self.should_stop():
            self.iterations += 1
            self.old_centroids = self.centroids.copy()
            self.get_labels()
            self.get_new_centroids()
        return self.centroids

    def should_stop(self):
        if self.iterations > self.max_iterations: 
            return True
        return (self.old_centroids == self.centroids).all()

    def get_labels(self):
        self.labels = np.apply_along_axis(lambda x: np.argmin(np.sqrt(np.sum((self.centroids - x)**2, axis=1))), 1, self.data)

    def get_new_centroids(self):
        for i in range(self.num_centroids):
            self.centroids[i] = (self.data[self.labels == i].mean(axis = 0))
