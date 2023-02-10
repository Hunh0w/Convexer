from scipy.spatial import ConvexHull, convex_hull_plot_2d
import matplotlib.pyplot as plt
import numpy as np
import math

def percentToLength(points, percentage: float):
    size = points.shape[0]
    return int(round(size * (1-percentage)))


def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

def getDistance(point, point2):
    distanceY = point[0] - point2[0]
    distanceX = point[1] - point2[1]
    return math.sqrt(distanceX**2 + distanceY**2)

def getMostFar(points, centeroid):
    mostFar = points[0]
    for point in points:
        mostFarDistance = getDistance(mostFar, centeroid)
        distance = getDistance(point, centeroid)
        if distance > mostFarDistance:
            mostFar = point
    return mostFar

def excludePoints(points, amount: int, centeroid):
    excludedPoints = []
    for i in range(amount):
        point = getMostFar(points,centeroid)
        index = np.where(points == point)[0][0]
        points = np.delete(points, index, 0)
        excludedPoints.append([point[0], point[1]])
    return np.array(excludedPoints), points

def convexPercent(points, percentage):
    centeroid = centeroidnp(points)
    amountToExclude = percentToLength(points, percentage)
    result = excludePoints(points, amountToExclude, centeroid)
    excludedPoints = result[0]
    points = result[1]

    if excludedPoints.size > 0:
        plt.plot(excludedPoints[:,0], excludedPoints[:,1], 'ro')
    plt.plot(*centeroid, 'r+')

    hull = ConvexHull(points)
    for simplex in hull.simplices:
        plt.plot(points[simplex, 0], points[simplex, 1], 'k-')



# Partitioning
def relationExists(relation, relations):
    for rel in relations:
        point1 = rel[0]
        point2 = rel[1]

        point3 = relation[0]
        point4 = relation[1]
        if point1[0] == point3[0] and point1[1] == point3[1] and point2[0] == point4[0] and point2[1] == point4[1]:
            return True
        if point1[0] == point4[0] and point1[1] == point4[1] and point2[0] == point3[0] and point2[1] == point3[1]:
            return True
    return False

def getRelations(point, relations):
    rels = []
    for relation in relations:
        point1 = relation[0]
        point2 = relation[1]
        if point1[0] == point[0] and point1[1] == point[1]:
            rels.append(relation)
            continue
        if point2[0] == point[0] and point2[1] == point[1]:
            rels.append(relation)
            continue
    return rels
def getSecondPoint(firstPoint, relation):
    p1 = relation[0]
    p2 = relation[1]
    if p1[0] == firstPoint[0] and p1[1] == firstPoint[1]:
        return p2
    else:
        return p1


# Utils
def getPercentageNumber(percentage_string):
    valid_number = percentage_string.replace("%", "")
    return float(valid_number) / 100

percentage_str = input("Pourcentage de points: ")
percentage_number = getPercentageNumber(percentage_str)

# Calculate Points
rng = np.random.default_rng()
points = rng.random((120, 2))

'''
points2 = rng.random((120, 2))
for p in points2:
    p[0] = p[0]+1
    p[1] = p[1]+1
points = np.concatenate((points, points2), 0)
'''

convexPercent(points, percentage_number)

'''
relations = []
for p1 in points:
    for p2 in points:
        if p1[0] == p2[0] and p1[1] == p2[1]:
            continue
        relation = [[p1[0], p1[1]], [p2[0], p2[1]]]
        if relationExists(relation, relations):
            continue
        distance = getDistance(p1, p2)
        if distance <= 0.20:
            relations.append(relation)
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo', linestyle="solid")

relations_displayed = []
for p1 in points:
    rels1 = getRelations(p1, relations)
    count1 = len(rels1)
    for relation in rels1:
        p2 = getSecondPoint(p1, relation)
        rels2 = getRelations(p2, relations)
        count2 = len(rels2)
        if(relationExists(relation, relations_displayed)):
            continue
        relations_displayed.append(relation)
        if count1 == 1 or count2 == 1:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'ro', linestyle="solid")
            print(count1)
            print(count2)
        else:
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo', linestyle="solid")
'''

plt.plot(points[:,0], points[:,1], 'o')    
plt.show()
#plt.savefig("convex_fig1.png")