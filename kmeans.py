


'''
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
'''
__author__ = 'Gordon Sun'
import sys, math, time, re
import random, csv, argparse
import numpy as np
import matplotlib.pyplot as plt
import csv
from operator import itemgetter
from datetime import datetime
from random import shuffle

column_headers = {
    1: 'dateTime',
    2: 'foods-log-caloriesIn',
    3: 'foods-log-water',
    4: 'activities-calories',
    5: 'activities-caloriesBMR',
    6: 'activities-steps',
    7: 'activities-distance',
    8: 'activities-floors',
    9: 'activities-elevation',
    10: 'activities-minutesSedentary',
    11: 'activities-minutesLightlyActive',
    12: 'activities-minutesFairlyActive',
    13: 'activities-minutesVeryActive',
    14: 'sleep-startTime',
    15: 'sleep-timeInBed',
    16: 'sleep-minutesAsleep',
    17: 'sleep-awakeningsCount',
    18: 'sleep-minutesAwake',
    19: 'sleep-minutesToFallAsleep',
    20: 'sleep-minutesAfterWakeup',
    21: 'sleep-efficiency',
    22: 'body-weight',
    23: 'body-bmi',
    24: 'body-fat'
}

column_headers2 = {
    0: 'dateTime',
    1: 'activities-calories',
    2: 'activities-caloriesBMR',
    3: 'activities-steps',
    4: 'activities-distance',
    5: 'activities-floors',
    6: 'activities-elevation',
    7: 'activities-minutesSedentary',
    8: 'activities-minutesLightlyActive',
    9: 'activities-minutesFairlyActive',
    10: 'activities-minutesVeryActive',
    11: 'sleep-timeInBed',
    12: 'sleep-minutesAsleep',
    13: 'sleep-awakeningsCount',
    14: 'sleep-minutesAwake',
    15: 'sleep-minutesToFallAsleep',
    16: 'sleep-minutesAfterWakeup',
}


# finds all instances of a search term within a search body and provides the start index of each of the terms.
# I: <string> search term, <string> search body
# O: True or False <bool> if the product is found
def find_category_presence(searchterm, searchbody):
    for x, item in enumerate(searchbody):
        if item == searchterm:
            return True
            break
    return False


# function to print a 2d list in terminal
# I:  array to be printed <list> 
# O:  field width or longest item length in the array
def print_2d_list(a):
    '''prints a 2D list in 2D form in the console'''
    if a == []:
        # So we don't crash accessing a[0]
        print []
        return
    rows, cols = len(a), len(a[0])
    field_width = max_item_length(a)
    print "[ ",
    for row in xrange(rows):
        if row > 0: print "\n  ",
        print "[ ",
        for col in xrange(cols):
            if col > 0: print ",",
            # The next 2 lines print a[row][col] with the given field_width
            formatted_array = "%" + str(field_width) + "s"
            print formatted_array % str(a[row][col]),
        print "]",
    print "]"


# function to help 2d list print; determines field width
# I:  array to be printed <list> 
# O:  field width or longest item length in the array
def max_item_length(a):
    '''returns the longest element length in the array'''
    max_len, rows, cols = 0, len(a), len(a[0])
    for row in xrange(rows):
        for col in xrange(cols):
            max_len = max(max_len, len(str(a[row][col])))
    return max_len


# Takes in a file and converts it to a 2D list
# I: filename <string> 
# O: outputs 2d <list> of <lists> 
# for this purpose, it also removes columns 21,24,2,3,14 to obtain the relevant data.
def read_table(filename):
    '''Takes in a file and converts it to a 2D list'''
    try:
        f = open(filename, 'r')
        data = f.readlines()
        file_contents = []
        for i, item in enumerate(data):
            row_n = (data[i].rstrip('\n').split(','))
            file_contents.append(row_n)
        for n_row, row in enumerate(file_contents):
            for x in xrange(0, 4):
                del row[len(row) - 1]  # remove 21-24
            for x2 in xrange(0, 2):
                del row[1]  # remove 2,3
            del row[11]  # remove14
        return file_contents
    except IOError:
        print('Error opening the file - file does not exist')
        sys.exit()


# function takes in a data file and returns the first row of the data set, assuming that it is the header
# I: <list> of <lists> 
# O: <list> of headers
def return_headers(datafile):
    return datafile[0]


# function reads in a data file and removes the first row of the data set.
# I: <list> of <lists> 
# O: <list> of <lists> minus the first row
def rm_headers(datafile):
    del datafile[0]
    return datafile


# function takes in two points of N dimensions and determines the Euclidean distance between the two points.
# I: <tuple> pt1, <tuple> pt2
# O: <float> distance
def distance(pt1, pt2):
    '''calculates the distance between two points'''
    if len(pt1) != len(pt2):
        print "Coordinate System Mismatch - dimen(pt1):" + str(len(pt1)) + "\tdimen(pt2):" + str(len(pt2)) + "\n"
        sys.exit()
    else:
        dist = 0
        for coord, pt1_item in enumerate(pt1):
            dist += (pt1_item - pt2[coord]) ** 2
        return math.sqrt(dist)


# function takes in an array of 2D tuples and determines the area of the polygon enclosed by the verticies.
# I: <list> of <tuples> 
# O: <float> area
# adapted from FB36; http://code.activestate.com/recipes/578047-area-of-polygon-using-shoelace-formula/
def shoelace(verticies):
    n = len(verticies)  # of points
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += verticies[i][0] * verticies[j][1]
        area -= verticies[j][0] * verticies[i][1]
    area = abs(area) / 2.0
    return area


# function takes in a array of 2D tuples and determines the ordering of the points such that the points are arranged in CCW direction
# I: <list> of <tuples> 
# O: sorted <list> of <tuples> 
# adapted from FB36; http://code.activestate.com/recipes/578047-area-of-polygon-using-shoelace-formula/
def PolygonOrderVertex(corners):
    # calculate centroid of the polygon
    n = len(corners)  # of corners
    cx = float(sum(x for x, y in corners)) / n
    cy = float(sum(y for x, y in corners)) / n
    # create a new list of corners which includes angles
    cornersWithAngles = []
    for x, y in corners:
        dx = x - cx
        dy = y - cy
        an = (math.atan2(dy, dx) + 2.0 * math.pi) % (2.0 * math.pi)
        cornersWithAngles.append([x, y, an])
    # sort it using the angles
    cornersWithAngles.sort(key=lambda tup: tup[2])
    return cornersWithAngles


# function pops on a new data point and removes old data point.
# I: <list> of <tuples> and <tuple> new point
# O: <list> of <tuples> 
def Pop_n_Q(window, new_dat):
    window.insert(len(window), new_dat)
    del window[0]
    return window


# This function returns the vector sum of two vectors x and y
def vector_sum(x, y):
    if len(x) != len(y):
        return None
    return [(x[i] + y[i]) for i in range(len(x))]


# This function returns the scalar product of a scalar a and vector x
def scalar_prod(a, x):
    return [a * x[i] for i in range(len(x))]


# function takes in the arguments for the script as well as provides a help interface for the program.
# Program accepts at minimum 3 arguments, but 3 arguments is allowed. Arguments accepted are:
# -i input file
# -o output filename.
# -w size of shifting window
# -m max iterations
# If no output filename arg is given, output file will be input_filename+.output suffix.
def get_args(args):
    parser = argparse.ArgumentParser(description='Run Program')
    parser.add_argument("-i", dest='input_file_name', help='Input filename', required=True)
    parser.add_argument('-w', dest='window', help='Define moving window size', required=True, default=7)
    parser.add_argument('-m', dest='maxIterations', help='Maximum number of iterations', default=100000)
    parser.add_argument('-o', dest='output_file_name', help='Output filename', default="")
    # parser.add_argument('-k', dest='k', help='Number of clusters', required = True)
    # If out is empty string, make it the input filename
    options = vars(parser.parse_args())
    if not options['output_file_name']:
        options['output_file_name'] = options['input_file_name'] + ".output"
    return options


# reads in the data from a filename and makes it into an array
def read_input_files(input_file_name):
    dat = read_table(input_file_name)
    dat = rm_headers(dat)
    dictionary = {k: list(v) for k, v in enumerate(zip(*dat))}
    for x, item in enumerate(dictionary[0]):
        # change date <str> to datetime format
        dictionary[0][x] = datetime.strptime(item, '%m/%d/%y')
    return dictionary


# This function selects desired data from the complete dataset and formats it for analysis.
def format_data_files(data_array):
    global_history = []
    selections = []
    time_depth = len(data_array[0])
    while True:
        dimen = raw_input("> Please enter the number of dimensions: ")
        try:
            dimen = int(dimen)

        except ValueError:
            print "> Please enter the number of dimensions (integer)."
            continue
        if dimen == 1:
            print "> 1D is not sufficient."
            continue
        else:
            break
    print ("> The following categories of data exist:\n" \
           "\t0 : 'dateTime'\n" \
           "\t1 : 'activities-calories'\n" \
           "\t2 : 'activities-caloriesBMR'\n" \
           "\t3 : 'activities-steps'\n" \
           "\t4 : 'activities-distance'\n" \
           "\t5 : 'activities-floors'\n" \
           "\t6 : 'activities-elevation'\n" \
           "\t7 : 'activities-minutesSedentary'\n" \
           "\t8 : 'activities-minutesLightlyActive'\n" \
           "\t9 : 'activities-minutesFairlyActive'\n" \
           "\t10 : 'activities-minutesVeryActive'\n" \
           "\t11 : 'sleep-timeInBed'\n" \
           "\t12 : 'sleep-minutesAsleep'\n" \
           "\t13 : 'sleep-awakeningsCount'\n" \
           "\t14 : 'sleep-minutesAwake'\n" \
           "\t15 : 'sleep-minutesToFallAsleep'\n" \
           "\t16 : 'sleep-minutesAfterWakeup'\n")
    print ("> Note: Category 0 (dateTime) is NOT included in the dataset.\n" \
           "> You must enter 0 for the dateTime category as a separate dimension\n" \
           "> Please select " + str(dimen) + " dimensions for analysis.")
    # User selection of unique categories for analysis.
    for d in xrange(dimen):
        while True:
            category = raw_input(
                "> Please select the category number you want to analyze (dimension " + str(d + 1) + "): ")
            try:
                category = int(category)
            except ValueError:
                print ("> Please enter a new integer from the list of categories above.\n" \
                       "\tYou have selected the following categories so far: \n" \
                       "\t" + str(selections))
                continue
            if 0 <= category < 17 and not find_category_presence(category, selections):
                selections.append(category)
                break
            else:
                print "> Please enter a unique category number between 0 and 16.\n"
    for d in xrange(time_depth):
        temp = []
        for s in xrange(len(selections)):
            temp.append(data_array[selections[s]][d])
        temp = map(float, temp)
        global_history.append(tuple(temp))
    return global_history


# function determines the distance between a point point and a line dictated by linepoint1 and linepoint2
def dist(linepoint1, linepoint2, point):
    x1 = linepoint1[0]
    y1 = linepoint1[1]

    x2 = linepoint2[0]
    y2 = linepoint2[1]

    x_0 = point[0]
    y_0 = point[1]

    return math.fabs(((y2 - y1) * x_0) - ((x2 - x1) * y_0) + (x2 * y1) - (y2 * x1)) / math.sqrt(
        ((y2 - y1) ** 2) + ((x2 - x1) ** 2))


# function determines the optimal # clusters given the SSEs
def find_elbow(SSEs):
    '''takes in array [k,sse]... and computes where the elbow is in the graph and the Ideal K'''
    first_point = SSEs[0]
    last_point = SSEs[len(SSEs) - 1]
    distances = []
    for x in range(len(SSEs)):
        distances.append(dist(first_point, last_point, SSEs[x]))
    return distances
    # return distances.index(max(distances))

# this class runs kmeans algorithm given a defined data set, k
class Kmeans():
    def __init__(self, args, k, data):
        options = get_args(args)
        self.maxIter = int(options['maxIterations'])
        self.k = k
        self.select_data = data
        [self.numPoints, self.numDimensions] = self.get_matrix_dimensions()
        self.centroids = self.generate_random_centroids()
        self.pointToCentroidMap = [None for i in range(self.numPoints)]

    def generate_random_centroids(self):
        '''picks a random point the data set for k clusters as random centroid'''
        indicies = range(len(self.select_data))
        shuffle(indicies)
        centroidIndexes = indicies[0: self.k]
        return [self.select_data[centroidIndexes[i]] for i in range(self.k)]

    def get_matrix_dimensions(self):
        '''returns the number of data points x number of dimensions; returns matrix dimensions'''
        numCols = len(self.select_data[0])
        numRows = len(self.select_data)
        return [numRows, numCols]

    def assign_points_to_centroids(self):
        changedAssignment = False  # keeps track if a point has changed clusters
        self.centroid2pointsMap = {}
        for i in range(self.numPoints):
            oldAssignment = self.pointToCentroidMap[i]

            closest_centroidindex = self.get_closest_centroid_index(self.select_data[i])
            self.pointToCentroidMap[i] = closest_centroidindex

            # update centroid to point mapping
            if not self.centroid2pointsMap.has_key(
                    closest_centroidindex):  # centroid does not have a list of assignees to it yet, create a fresh list
                self.centroid2pointsMap[closest_centroidindex] = [i]
            else:
                self.centroid2pointsMap[closest_centroidindex].append(i)

            # check if datapoint changed cluster
            if oldAssignment != self.pointToCentroidMap[i]:
                changedAssignment = True

        return changedAssignment

    def get_closest_centroid_index(self, dataPoint):
        '''Returns the index (cluster number) of the closest centroid to a data point'''
        minDist = float('inf')
        closestCentroidIndex = None

        # iterate over each centroid and keep track of the one with
        # the closest distance
        for i in range(self.k):
            # print self.centroids[i]
            d = distance(dataPoint, self.centroids[i])

            if d < minDist:
                minDist = d
                closestCentroidIndex = i

        return closestCentroidIndex

    def recompute_centroids(self):
        # iterate over all centroids
        for i in range(self.k):
            # if centroid has any datapoints assigned to it then recompute; else do nothing
            if self.centroid2pointsMap.has_key(i):
                numPointsInCluster = len(self.centroid2pointsMap[i])
                newCentroid = [0.0 for iteration in range(self.numDimensions)]

                #  vector sum of all data points assigned to centroid and average coordinage to get new centroid
                for j in self.centroid2pointsMap[i]:
                    newCentroid = vector_sum(newCentroid, self.select_data[j])

                newCentroid = scalar_prod(1.0 / numPointsInCluster, newCentroid)

                self.centroids[i] = newCentroid

    # runs the KMeans algorithm
    def run(self):
        # run KMeans at most maxIters if it does not converge
        for itr in range(self.maxIter):
            # step 1: assign data points to centroids, return value, determine whether any datapoint changed clusters
            changedAssignments = self.assign_points_to_centroids()

            # convergence test: if no datapoint changed assigned cluster then KMeans has converged, centroids will not change, so  break the loop
            if not changedAssignments:
                break
            # step 2: recompute the centroids based on the assigned datapoints to each cluster
            self.recompute_centroids()

    def simple_report_results(self):
        results = ""
        print "DataPtNum\tClusterNum"
        for i in range(self.numPoints):
            results += str(i + 1) + "\t" + str(self.pointToCentroidMap[i]) + "\n"
        results = results.strip()
        print results

    def mega_dump(self):
        result = []
        # print "DataPoint\tClusterNum\tCentroidPoint"
        for i in range(self.numPoints):
            # print [self.select_data[i], self.pointToCentroidMap[i]+1,tuple(self.centroids[self.pointToCentroidMap[i]])]
            result.append([self.select_data[i], self.pointToCentroidMap[i] + 1,
                           tuple(self.centroids[self.pointToCentroidMap[i]])])
        return result

    def __str__(self):
        return "\n******************" + "\n\n" + \
               "k : " + str(self.k) + "\n" + \
               "maxIters : " + str(self.maxIter) + "\n" + \
               "******************\n";

    def SSE(self):
        dataset = self.mega_dump()
        SumSqErrors = 0
        for i in range(len(dataset)):
            SumSqErrors += distance(dataset[i][0], dataset[i][2]) ** 2
        return SumSqErrors


def main(args):

    options = get_args(args)

    output_filename = options['output_file_name']
    outputfile_centroids = open(str(output_filename + "_centroids"), "w")
    outputfile_points = open(str(output_filename + "_points"), "w")
    outputfile_TraceMap = open(str(output_filename + "_TraceMap"), "w")
    outputfile_area = open(str(output_filename + "_area.csv"), "w")
    # columns for tracemap are  Datapoint, cluster #, cluster coordinate--note cluster number is not preserved among windows

    data_input = read_input_files(options['input_file_name'])
    data_input = format_data_files(data_input)

    window_size = int(options['window'])

    if window_size > len(data_input):
        print "> Error: Window size exceeds that of the dataset"
        sys.exit()

    toodee = False
    if len(data_input[0]) == 2:
        toodee = True

    numScans = len(data_input) - window_size + 1

    sse_one_array = [[i+1] for i in xrange(window_size)]
    distances = [[g+1] for g in xrange(window_size)]

    centroid_evolution = []
    # for each window
    for x in range(numScans):
        # Write window number
        outputfile_centroids.write("> Window " + str(x + 1) + " Clusters >>>>>>>>>>>>>>>>\n")
        outputfile_points.write("> Window " + str(x + 1) + " Points >>>>>>>>>>>>>>>>\n")

        # sample the dataset for the window
        window_data = data_input[x:x + window_size]
        # write points to output file
        for x3, item in enumerate(window_data):
            outputfile_points.write(str(item)[1:len(str(item)) - 1] + "\n")

        # for the size of the window compute the ideal k
        SSEs = []
        for x2 in range(window_size):
            k_size_means = Kmeans(options, x2 + 1, window_data)
            k_size_means.run()
            SSEs.append([x2 + 1, k_size_means.SSE()])
        dist = find_elbow(SSEs)


        # store sse and sse distance data for elbow verification in plotting
        for x39, item in enumerate(SSEs):
            sse_one_array[x39].append(item[1])
        for x40, item in enumerate(dist):
            distances[x40].append(item)

        optimal_k = dist.index(max(dist))

        # actually run the k means at optimal K
        k_means_run = Kmeans(options, optimal_k + 1, window_data)
        k_means_run.run()

        outputfile_TraceMap.write("> Window " + str(x + 1) + " Tracemap >>>>>>>>>>>>>>>>\n")
        for x4, item in enumerate(k_means_run.mega_dump()):
            outputfile_TraceMap.write(str(item)[1:len(str(item)) - 1] + "\n")

        # if data is in 2D, sort centroids in CCW order
        if toodee:
            ordered_centroid_points = PolygonOrderVertex(k_means_run.centroids)
            formatted_ordered_ctd_pts = []
            for x10, item in enumerate(ordered_centroid_points):
                del item[-1]
                formatted_ordered_ctd_pts.append(tuple(item))
            area = shoelace(formatted_ordered_ctd_pts)
            outputfile_area.write(str(area)+"\n")
        else:
            formatted_ordered_ctd_pts = k_means_run.centroids

        # write centroid points to data file
        for x8, item in enumerate(formatted_ordered_ctd_pts):
            outputfile_centroids.write(str(item)[1:len(str(item)) - 1] + "\n")

        centroid_evolution.append(formatted_ordered_ctd_pts)

    with open(str(output_filename + "_SSE.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerows(sse_one_array)

    with open(str(output_filename + "_SSE_dist.csv"), "wb") as f:
        writer = csv.writer(f)
        writer.writerows(distances)

    outputfile_centroids.close()
    outputfile_points.close()
    outputfile_TraceMap.close()
    outputfile_area.close()

    print "> Program done running"
    sys.exit()

if __name__ == '__main__':
    main(sys.argv)
