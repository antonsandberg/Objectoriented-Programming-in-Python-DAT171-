import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.sparse import csr_matrix
import numpy as np
from scipy.sparse.csgraph import shortest_path
import time
from scipy.spatial import cKDTree
""" Assignment 1
Author: Anton Sandberg (2021) and Oliver Johansson (2021), 
    antsandb@student.chalmers.se and olijoh@student.chalmers.se """


def read_coordinate_file(filename):
    """ Reads the given coordinate file and parses the results into an array of coordinates

    :param filename: File with coordinates
    :type filename: txt

    :return coords: returns the coordinates in an array format
    :rtype coords: ndarray
    """

    start = time.time()
    r = 1
    # Pre creating the list
    coords = []

    with open(filename) as f:
        for line in f:
            line = line.replace('{', '')
            line = line.replace('}', '')
            line = line.strip().split(',')

            x = r*np.pi*float(line[1])/180  # Changing the variables from given instructions
            y = r*np.log(np.tan(np.pi/4 + np.pi*float(line[0])/360))

            coords.append((x, y))

    end = time.time()
    time1 = end - start
    print("Time of read_coordinate_file : %.6f" % time1)

    return np.array(coords)


def plot_points(coord_list, indices, path):
    """ Plots the data points read from the file

    :param coord_list: The coordinates for all cities
    :param indices: The pairs that are in range
    :param path: shortest path from start to end city
    :type coord_list: ndarray
    :type indices: ndarray
    :type path: ndarray

    """

    start = time.time()
    x = []
    y = []  # Pre creating the lists

    for i in coord_list:
        x.append(i[0])
        y.append(i[1])  # Separating x and y coordinates

    lines = LineCollection(coord_list[indices], linewidths=0.2, colors='grey')
    fig, ax = plt.subplots()
    ax.add_collection(lines)
    ax.scatter(x, y, s=7, c='r')

    x_path = []
    y_path = []

    for [x_c, y_c] in coord_list[path]:
        x_path.append(x_c)
        y_path.append(y_c)

    ax.plot(x_path, y_path)

    end = time.time()
    time2 = end - start
    print("Time of plt_points  : %.7f" % time2)

    plt.title("Shortest Path")

    plt.show()


def construct_graph_connections(coord_list, radius):
    """ Computes all the connections between all the points
    in coord_list that are within the radius given

    :param coord_list: the coordinate list for respective city
    :param radius: The radius which will be checked
    :type coord_list: ndarray
    :type radius: float

    :return links: Every pair that's within range
    :return distances: All the pair's distance
    :rtype links: ndarray
    :rtype distances: ndarray
    """

    start = time.time()
    # Pre create the lists
    links = []
    distances = []

    # Use enumerate to be able to check distance in between the coordinates
    for city, coords1 in enumerate(coord_list):
        for near_city, coords2 in enumerate(coord_list):
            dist = np.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)
            if dist < radius and city != near_city:
                links.append((city, near_city))

                distances.append(dist)

    end = time.time()
    time3 = end - start
    print("Time of construct_graph_connections  : %.3f" % time3)

    return np.array(links), np.array(distances)


def construct_fast_graph_connections(coord_list, radius):
    """ Computes all the connections between all the points
    in coord_list that are within the radius given but faster

    :param coord_list: the coordinate list for respective city
    :param radius: The radius which will be checked
    :type coord_list: ndarray
    :type radius: float

    :return links: Every pair that's within range
    :return distances: All the pair's distance
    :rtype links: ndarray
    :rtype distances: ndarray
    """

    start = time.time()
    # Pre create the lists
    distances = []
    pairs = []

    # Uses cKDTree to cut down on time
    tree = cKDTree(coord_list)
    links = tree.query_ball_tree(tree, radius)

    # After the above use the same thought process to create the pairs as well as check distance
    for city, near_cities in enumerate(links):
        for near_city in near_cities:
            if city != near_city:
                dist = np.sqrt((coord_list[city][0] - coord_list[near_city][0]) ** 2 + (coord_list[city][1] - coord_list[near_city][1]) ** 2)
                distances.append(dist)
                pairs.append((city, near_city))

    end = time.time()
    time4 = end - start
    print("Time of construct_fast_graph_connections  : %.3f" % time4)

    return np.array(pairs), np.array(distances)


def construct_graph(indices, distance, N):
    """ Constructing the sparse graph

    :param indices: The pairs that are in range
    :param distance: The distances between all the pairs
    :param N: len(coords_list)
    :type indices: ndarray
    :type distance: ndarray
    :type N: int

    :return matrix: The pairs and it's distance
    :rtype matrix: ndarray

    """

    start = time.time()
    # Pre create the lists
    row = []
    col = []

    for k in indices:
        row.append(k[0])
        col.append(k[1])

    # Use csr_matrix as instructed
    matrix = csr_matrix((distance, (row, col)), shape=(N, N))

    end = time.time()
    time5 = end - start
    print("Time of construct_graph  : %.3f" % time5)

    return matrix


def find_shortest_path(graph, start):
    """ Finds the shortest paths from start to all other cities

    :param graph: The pairs and it's distance
    :param start: The start city
    :type graph: ndarray
    :type start: int

    :return path: The shortest path from start to all other cities
    :return predecessor: Previous city when taking the shortest path to the given column index
    :rtype path: ndarray
    :rtype predecessor: ndarray

    """

    start1 = time.time()
    path, predecessor = shortest_path(graph, indices=start, return_predecessors=True)

    end = time.time()
    time6 = end - start1
    print("Time of find_shortest_path  : %.3f" % time6)

    return path, predecessor



def compute_path(predecessor_matrix, start_node, end_node):
    """ converts the shortest path to a sequence of nodes that represent it

    :param predecessor_matrix: Previous city when taking the shortest path to the given column index
    :param start_node: The city which to start on
    :param end_node: The city which to end on
    :type predecessor_matrix: ndarray
    :type start_node: int
    :type end_node: int

    :return path_seq: shortest path from start to end city
    :rtype path_seq: ndarray
    """

    start = time.time()

    path_seq = [end_node]
    new_node = end_node

    while new_node != start_node:
        new_node = predecessor_matrix[new_node]
        path_seq.append(new_node)
    path_seq = np.flip(path_seq)

    end = time.time()
    time7 = end - start
    print("Time of compute_path  : %.3f" % time7)

    return path_seq


# The actual code that's run
if __name__ == "__main__":

    FILENAMES = ['SampleCoordinates.txt', 'HungaryCities.txt', 'GermanyCities.txt']
    START_NODES = [0, 311, 1573]
    END_NODES = [5, 702, 10584]
    RADIUS = [0.08, 0.005, 0.0025]  # All given in the assignment

    # Change the index of all the list files to the correct file number
    # 0 = SampleCoordinates
    # 1 = HungaryCoordinates
    # 2 = GermanyCoordinates
    coord_list = read_coordinate_file(FILENAMES[0])

    connections, distances = construct_graph_connections(coord_list, RADIUS[0])

    # Naming these "fast" to keep track on which is which
    connectionsfast, distancesfast = construct_fast_graph_connections(coord_list, RADIUS[0])

    N = len(coord_list)

    graph_matrix = construct_graph(connectionsfast, distancesfast, N)

    path, predecessor = find_shortest_path(graph_matrix, START_NODES[0])

    path_seq = compute_path(predecessor, START_NODES[0], END_NODES[0])

    plot_points(coord_list, connectionsfast, path_seq)

    print("Shortest path from {} and {} is: {}".format(START_NODES[0], END_NODES[0], path_seq))
    print("And total distance is: {}".format(path[END_NODES[0]]))