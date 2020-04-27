import re

import numpy as np
from queue import PriorityQueue
import itertools

from path_finder.extra_tools import distance


class Playground:
    def __init__(self, filepath=None, shape=None):
        self.board = None
        self.center = None
        self.points_pq = []
        self.next_value = int(1)
        if filepath:
            self.load_file(filepath)
        elif shape is not None:
            self.board = np.zeros(shape)
            self.center = (self.board.shape[0] // 2, self.board.shape[1] // 2)

        self.invalid_nodes = set()
        self.paths = []
        self.current_pp = None
        self.aborted_pp = []

    def set_pp(self):
        """
        Sets a valid PointPair value as current_pp.
        current_pp is the pair of coordinates pointing to the same value in the board
        :return: boolean, True if game is still on, False if there is no pair left
        """
        if self.current_pp and not self.current_pp.completed:
            return True
        if len(self.points_pq):
            self.current_pp = self.points_pq.pop()
            return True
        elif len(self.aborted_pp):
            self.current_pp = self.aborted_pp.pop()
            return True
        return False

    def add_points(self, pair1, pair2):
        """
        Adds a new pair of points to the playground having value equal to next_value
        Updates the board, points_pq and increments next_value
        :param pair1: tuple (x-coordinate, y-coordinate)
        :param pair2: tuple (x-coordinate, y-coordinate)
        :return: void
        """
        self.points_pq.append(PointPair(np.array(pair1), np.array(pair2), self.next_value, self.center))
        self.board[pair1] = self.next_value
        self.board[pair2] = self.next_value
        self.points_pq.sort()
        self.next_value += 1

    def go_one_step(self):
        """
        Advance one step with the current PointPair
        One step is added to the path leaving from coordinate x, one step is added to the path from Y
        :return: void
        """
        self.a_star_steps(self.current_pp)

    def save_to_csv(self, filename):
        """
        Save board configuration to csv file
        :param filename: str
        :return: void
        """
        np.savetxt(re.sub('.csv', '', filename) + '.csv', self.board.astype('int'), delimiter=",", fmt='%d')

    def find_paths(self):
        """
        Find paths for all pairs of coordinates left uncompleted
        :return: void
        """
        while self.set_pp():
            self.a_star()

    def load_file(self, filepath):
        """
        Load playground from csv file
        Initialize list of points sorted in the order in which paths should be computed
        :param filepath: str
        :return: void
        """
        self.board = np.genfromtxt(filepath, delimiter=',', dtype='int')
        self.center = (self.board.shape[0] // 2, self.board.shape[1] // 2)
        # load coordinates of non zero values
        coordinates = np.argwhere(self.board)
        # sort by value at coordinates
        coordinates = coordinates[
            np.argsort(np.apply_along_axis(
                lambda row: self.board[row[0], row[1]],
                1,
                coordinates))
        ]

        for pair in zip(*[iter(coordinates)] * 2):
            self.points_pq.append(PointPair(pair[0], pair[1], self.board[pair[0][0], pair[0][1]], self.center))
        self.points_pq.sort()
        self.next_value = len(self.points_pq) + 1

    def get_neighbours(self, x):
        """
        Get coordinates of all neighbours around a given point, including diagonal neighbours
        Coordinates are included in the board's shape
        :param x: tuple (x-coordinate, y-coordinate)
        :return: list of tuples (x-coordinate, y-coordinate)
        """
        vert = [x[0], x[0] - 1, x[0] + 1]
        horz = [x[1], x[1] - 1, x[1] + 1]
        neighbours = []
        for point in itertools.product(vert, horz):
            if not np.any(np.array(point) < 0) \
                    and not np.any(np.array(point) >= self.board.shape) \
                    and not np.array_equal(point, x):
                neighbours.append(point)
        return neighbours

    def get_orthogonal_neighbours(self, x):
        """
        Get coordinates of neighbours found on the same row on column with x
        :param x: tuple (x-coordinate, y-coordinate)
        :return: list of tuples (x-coordinate, y-coordinate)
        """
        neighbours = [
            point for point in
            [(x[0] - 1, x[1]), (x[0] + 1, x[1]), (x[0], x[1] - 1), (x[0], x[1] + 1)]
            if not np.any(np.array(point) < 0) and not np.any(np.array(point) >= self.board.shape)
        ]
        return neighbours

    def is_valid(self, point, path, tried_pins):
        """
        Check validity of a point in the current board given the path in which it will be incorporated
        and the points that were formerly tried
        :param point: tuple (x-coordinate, y-coordinate)
        :param path: list of tuples (x-coordinate, y-coordinate) representing contiguous coordinates in the path
        :param tried_pins: set of tuples(x-coordinate, y-coordinate)
        :return: boolean: True if point is valid, False otherwise
        """
        # 1. Check that it is in the board
        if np.any(np.array(point) < 0) or np.any(np.array(point) >= self.board.shape):
            return False
        # 2. Check that it does not point to a pin with another value
        if self.board[point] not in [0, self.board[path[0]]]:
            return False
        # 2. Check that it is not between two orthogonally neighbouring pins having any value other than 0
        neighbours = self.get_orthogonal_neighbours(point)
        pin_counter = 0
        for n in neighbours:
            pin_counter += self.board[n] != 0
        if pin_counter > 1:
            return False
        # 3. Check that it is not part of an existing path or near it
        if (point[0], point[1]) in self.invalid_nodes:
            return False
        # 4. Check that it was not already tried for the current path
        if point in tried_pins:
            return False
        # 5. Check that it is not near a pin with another number
        neighbours = self.get_neighbours(point)
        # 6. Check that it is not a neighbour of more than 2 pins that are already part of the path
        counter = 0
        for n in neighbours:
            point_value = self.board[n]
            if point_value != 0 and point_value != self.board[path[0]]:
                return False
            counter += n in tried_pins
            if counter > 2:
                return False
        # 7. Check that the step is not redundant
        if len(path) > 3:
            last = path[-3:]
            if last[-1][0] != point[0] and last[-1][1] != point[1]:
                if last[-2][0] == point[0] and last[-3][0] == point[0]:
                    return False
                if last[-2][1] == point[1] and last[-3][1] == point[1]:
                    return False
        return True

    def next_steps(self, y, path, tried_pins):
        """
        Get a list of valid next steps for the given path
        :param y: tuple (x-coordinate, y-coordinate) representing the coordinates of the seeking destination
        :param path: list of tuples (x-coordinate, y-coordinate) representing contiguous coordinates in the path
        :param tried_pins: set of tuples(x-coordinate, y-coordinate)
        :return:
        """
        steps = []
        x = path[-1]
        for point in self.get_neighbours(x):
            if self.is_valid(point, path, tried_pins):
                new_path = path[:]
                new_path.append(point)
                steps.append(Step(point, x, y, new_path, self.center))
        return steps

    def update_playground(self, path, value):
        """
        Update the playground with a new path: paths, invalid nodes and board
        :param path: list of tuples (x-coordinate, y-coordinate) representing contiguous coordinates in the path
        :param value: int, value drawn by the path
        :return: void
        """
        self.paths.append(path)
        for coords in path:
            self.invalid_nodes.add(coords)
            self.board[coords] = value
            for n in self.get_neighbours(coords):
                self.invalid_nodes.add(n)

    def a_star(self):
        """
        Apply a-star algorithm on both coordinates in the current pair of coordinates until path is completed
        :return: void
        """
        while not self.current_pp.completed:
            self.a_star_steps(self.current_pp)

    def a_star_steps(self, pp):
        """
        Advance one step with a-star algorithm on both paths starting from the current pair of coordinates
        If after advancing one step the two paths have neighbouring limits,
        i.e. the limits are at a distance of 1 empty cell and can be found on the same row or column
        or the limits are diagonally neighbouring each other,
        the path is completed by combining the two paths
        :param pp: PointPair
        :return: void
        """
        self.a_star_step(pp, 0)
        self.a_star_step(pp, 1)
        if pp.completed:
            return
        x_limit = pp.path[0][-1]
        y_limit = pp.path[1][-1]
        if distance(np.array(x_limit), np.array(y_limit)) == 2:
            if x_limit[0] == y_limit[0]:
                pp.final_path = pp.path[0] + [(x_limit[0], (x_limit[1] + y_limit[1]) // 2)] + pp.path[1][::-1]
                pp.completed = True
                self.update_playground(pp.final_path, pp.value)
            elif x_limit[1] == y_limit[1]:
                pp.final_path = pp.path[0] + [((x_limit[0] + y_limit[0]) // 2, x_limit[1])] + pp.path[1][::-1]
                pp.completed = True
                self.update_playground(pp.final_path, pp.value)
        neighbours = self.get_neighbours(pp.path[0][-1])
        if pp.path[1][-1] in neighbours:
            pp.final_path = pp.path[0] + pp.path[1][::-1]
            pp.completed = True
            self.update_playground(pp.final_path, pp.value)

    def a_star_step(self, pp, index):
        """
        Add possible new steps from the current position to the priority queue
        Pop the next step having the highest priority (lowest combined distance)
        If priority queue remain empty, return with a final path containing only the pin points in PointPair,
        set the PointPair as completed and update playground
        If the path reaches its destination, update final_path, completed flag and playground
        :param pp: PointPair
        :param index: 0 if step for path starting from x is wanted, 1 if step for path starting from y is wanted
        :return: void
        """
        if np.array_equal(pp.current_point[index], pp.limits[(index + 1) % 2]):
            return
        pp.tried_pins[index].add((pp.current_point[index][0], pp.current_point[index][1]))
        further_steps = self.next_steps(pp.limits[(index + 1) % 2],
                                        pp.path[index],
                                        pp.tried_pins[index])
        for step in further_steps:
            pp.pq[index].put(step)
        if pp.pq[index].qsize() == 0:
            pp.completed = True
            pp.aborted = True
            pp.final_path = [(pp.x[0], pp.x[1]), (pp.y[0], pp.y[1])]
            self.aborted_pp.append(pp)
            return
        step = pp.pq[index].get()
        pp.current_point[index] = step.coords
        pp.path[index] = step.path[:]
        if np.array_equal(pp.current_point[index], pp.limits[(index + 1) % 2]):
            pp.completed = True
            pp.final_path = pp.path[index][:]
            self.update_playground(pp.path[index], pp.value)


class Step:
    def __init__(self, coords, x, y, path, board_center):
        self.coords = coords
        self.prev = x
        self.path = path
        self.dist = distance(np.array(x), np.array(coords))
        self.combined_dist = (
                distance(np.array(coords), np.array(y))
                + distance(np.array(coords), np.array(x))
                - 0.50 * distance(np.array(coords), np.array([board_center[0], board_center[1]]))
        )

    def __str__(self):
        return f'({self.coords[0]}, {self.coords[1]}), dist: {self.dist}, combined_dist: {self.combined_dist}'

    def __lt__(self, other):
        return self.combined_dist < other.combined_dist


class PointPair:
    """
    Class that represents the state of a pair of two pins having the same value and the paths that connect them
    """
    def __init__(self, x, y, value, board_center):
        # coordinates of the pins
        self.x = x
        self.y = y
        # limits of the current paths
        self.limits = [x, y]
        # value of the pins
        self.value = value
        # distance between the two pins
        self.d = distance(x, y)
        # total distance from center to x and center to y
        self.center_d = (distance(x, np.array([board_center[0], board_center[1]])) +
                         distance(y, np.array([board_center[0], board_center[1]]))) / 2
        # path[index] - path starting from x if index = 0, y if index = 1
        self.path = [[(x[0], x[1])], [(y[0], y[1])]]
        # pq[index] - priority queue of next steps given index = 0 for x, 1 for y
        self.pq = [PriorityQueue(), PriorityQueue()]
        # current limits of the paths
        self.current_point = [x, y]
        # points that were tried in the process of building the paths
        self.tried_pins = [set(), set()]
        # flag: True if path is completed
        self.completed = False
        # flag: True if aborted
        self.aborted = False

    def __lt__(self, other):
        """
        Prioritize the selection of pairs of points
        """
        # return self.d > other.d
        return self.d - 0.15 * self.center_d > other.d - 0.15 * other.center_d
        # other.center_d + 
        # and self.d > other.d
