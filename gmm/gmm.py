from sklearn.mixture import GaussianMixture as GMM
import pandas as pd

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

def gmm(points):
    gmm = GMM(n_components=2).fit(points)
    gmm.fit(points)
