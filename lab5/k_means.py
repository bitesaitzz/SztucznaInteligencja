import numpy as np


def initialize_centroids_forgy(data, k):
    # TODO implement random initialization
    n_samples = data.shape[0]
    random_indices = np.random.permutation(n_samples)[:k]
    centroids = data[random_indices]
    return centroids


def initialize_centroids_kmeans_pp(data, k):
    # TODO implement kmeans++ initizalization
    centroids = np.zeros((k, data.shape[1]))
    centroids[0] = data[np.random.choice(data.shape[0]), :]
    for i in range(1, k):
        distances = np.sqrt(((data - centroids[:i, np.newaxis]) ** 2).sum(axis=2))
        prob = distances.min(axis=0) ** 2
        prob /= prob.sum()
        new_centroid_index = np.random.choice(data.shape[0], p=prob)
        centroids[i] = data[new_centroid_index]

    return centroids


def assign_to_cluster(data, centroids):
    # TODO find the closest cluster for each data point
    distances = np.sqrt(((data[:, np.newaxis] - centroids) ** 2).sum(axis=2))
    # distances = np.linalg.norm(data[:, np.newaxis] - centroids, axis=2)
    assignments = np.argmin(distances, axis=1)
    return assignments


def update_centroids(data, assignments):
    # TODO find new centroids based on the assignments
    unique_clusters = np.unique(assignments)
    centroids = np.zeros((len(unique_clusters), data.shape[1]))

    for i, cluster in enumerate(unique_clusters):
        cluster_data = data[assignments == cluster]
        centroid = np.mean(cluster_data, axis=0)
        centroids[i] = centroid
    return centroids
def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :])**2))

def k_means(data, num_centroids, kmeansplusplus= False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    
    assignments  = assign_to_cluster(data, centroids)
    for i in range(100): # max number of iteration = 100
        #print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments): # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)         

