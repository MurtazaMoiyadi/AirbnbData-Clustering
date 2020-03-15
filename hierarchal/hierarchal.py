from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
import scipy.cluster.hierarchy as sch

def get_points(dataset):
    """ Accepts the nyclistings dataset and returns a list of points
        that include latitude, longitude, and price.
    """
    data = pd.read_csv(dataset)
    points = []
    for i in range(len(data.index)):
        point = []
        latitude = float(data["latitude"][i])
        longitude = float(data["longitude"][i])
        price = int(data["price"][i])
        point += [latitude, longitude, price]
        points += [point]
    
    
    return points

def clustering(points):
    """ Utilizes sklearn to implement Agglomerative heirarchal 
        clustering
    """
    clustering = AgglomerativeClustering(n_clusters = 2, affinity='euclidean', linkage='ward').fit_predict(points)
    return clustering

def dendogram(points, clusterlabel):
    """plots the clusters to visualize the results of
        heirarchal clustering
    """
    #p = pd.DataFrame(points, columns=["Lat", "Long", "Price"])
    lat = []
    long = []
    price = []
    for i in range(len(points)):
        lat.append(points[i][0])
        long.append(points[i][1])
        price.append(points[i][2])
    plt.figure(figsize=(10, 7))
    plt.title("Dendogram")
    dend = sch.dendrogram(sch.linkage(points, method='ward'))