import sys
import math
import numpy as np
import scipy.io.wavfile


class Centroid:
    _location = None
    _assigned_points = []

    def __init__(self, init_location):
        self._location = init_location
        self._assigned_points = []

    def get_location(self):
        return self._location

    def assign_point(self, point):
        self._assigned_points.append(point)

    def clear_points(self):
        self._assigned_points = []

    def update_location(self):
        new_location = [0, 0]
        size = self._assigned_points.__len__()
        # Update centroid to be the average of the points in its cluster
        for point in self._assigned_points:
            new_location[0] = new_location[0] + point[0]
            new_location[1] = new_location[1] + point[1]

        if size != 0:
            new_location[0] /= size
            new_location[1] /= size

        new_location[0] = round(new_location[0])
        new_location[1] = round(new_location[1])


        if (self._location[0] != new_location[0] or self._location[1] != new_location[1]):
            # update the centroid location
            self._location = new_location
            return False
        return True


def distance(x1, x2):
    return math.sqrt(pow(x1[0] - x2[0], 2) + pow(x1[1] - x2[1], 2))


def main():
    sample, centroids = sys.argv[1], sys.argv[2]  # reading
    fs, y = scipy.io.wavfile.read(sample)
    x = np.array(y.copy())  # data
    initial_centroids = np.loadtxt(centroids)  # centroids

    # the K value is the num of points in the centroid file
    k = len(initial_centroids)

    # Create for each centroid his own list of points and put all the centroids in a list

    centroids = []
    for cent in initial_centroids:
        centroids.append(Centroid(cent))

    f = open("output.txt", "a")

    is_convergence = False
    i = 0
    # do 30 iterations
    while not is_convergence and i < 30:
        is_convergence = True
        # assign each point to the closest centroid to him
        for point in x:
            min_dist = distance(point, centroids[0].get_location())
            new_cent = centroids[0]
            for cent in centroids:
                dist = distance(point, cent.get_location())
                if dist < min_dist:
                    min_dist = dist
                    new_cent = cent
            new_cent.assign_point(point)

        # update all the centroids location
        for cent in centroids:
            changed = cent.update_location()
            if (changed == False):
                is_convergence = False

        # Print the centroids in each iteration
        arr = np.array(cent.get_location())
        print(f"[iter {i}]:{','.join([str(arr) for cent in centroids])}")
        f.write(f"[iter {i}]:{','.join([str(arr) for cent in centroids])}")
        f.write("\n")
        i += 1

        # clear all the assigned points
        for cent in centroids:
            cent.clear_points()

    f.close()


main()
