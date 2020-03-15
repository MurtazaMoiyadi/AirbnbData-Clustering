from collections import defaultdict
from math import inf
import random
import pandas as pd
import matplotlib.pyplot as plt


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
        

def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    n = len(points)
    x = sum([float(p[0]) for p in points]) / n
    y = sum([float(p[1]) for p in points]) / n
    z = sum([int(p[2]) for p in points]) / n
    return [x, y, z]


def update_centers(points, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    k = int(max(assignments) + 1)
    clusters = [[] for i in range(k)]
    for pointIndex, pointAssignment in enumerate(assignments):
        clusters[round(pointAssignment)].append(points[round(pointIndex)])

    new_centers = []
    for cluster in clusters:
        if len(cluster) != 0:
            new_centers.append(point_avg(cluster))

    return new_centers

def assign_points(points, centers):
    """ Assigns points to centers based on kmeanspp
    """
    assignments = []
    for point in points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    return sum([(a - b) ** 2 for a, b in zip(a, b)]) ** 0.5


def distance_squared(a, b):
    return distance(a, b) ** 2


def cost_function(clustering):
    cost = 0
    for each in clustering:
        center = point_avg(clustering[each])
        cost += sum([distance_squared(center, p) for p in clustering[each]])

    return cost


def generate_k_pp(points, k):
    center = random.choice(points)
    k_points = [center]

    while len(k_points) < k:
        prob = []
        for point in points:
            prob.append(distance_squared(center, point))
        
        prob = [p/sum(prob) for p in prob]
        center = random.choices(points, prob)[0]

        k_points.append(center)

    return k_points


def _do_lloyds_algo(points, k_points):
    assignments = assign_points(points, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(points, assignments)
        old_assignments = assignments
        assignments = assign_points(points, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, points):
        clustering[assignment].append(point)
    return clustering


def k_means_pp(points, k):
    if k not in range(1, len(points)+1):
        raise ValueError("lengths must be in [1, len(dataset)]")

    k_points = generate_k_pp(points, k)
    return _do_lloyds_algo(points, k_points)


def plot(points, cluster):
    """ Plots longitude and longitude of the listings
    """
    df = pd.DataFrame(points, columns=['latitude','longitude','price'])
    plt.scatter(df['latitude'],df['longitude'], c=cluster, cmap='rainbow')


def avg_price(points, a):
    """computes the average price of listings within each cluster
    """
    if len(points) != len(a):
        raise ValueError('Arguments must have same length')
    sum0 = 0
    sum1 = 0 
    count0 = 0
    count1 = 0
    for i in range(len(points)):
        if a[i] == 0:
            count0 += 1
            sum0 += points[i][2]
        else:
            count1 += 1
            sum1 += points[i][2]
    avg0 = sum0/count0
    avg1 = sum1/count1
    return [avg0, avg1]

            
    
def cost_plot(dataset):
    points = get_points(dataset)
    plt.xlabel('k') 
    plt.ylabel('cost')
    plt.title('Cost Analysis')
    cost = []
    k = [1, 2, 3, 4]
    for i in k:
        cluster = k_means_pp(points, i)
        cost.append(cost_function(cluster))
    plt.plot(k, cost)
    plt.show()