import numpy as np
from queue import PriorityQueue
import itertools

from brute_force.printing_tools import print_pretty_table, distance


class Playground:
    def __init__(self, filepath):
        self.board = None
        self.center = None
        self.points_pq = []
        self.load_file(filepath)

        self.invalid_nodes = set()
        self.paths = []
        self.current_pp = None

    def set_pp(self):
        if self.current_pp and not self.current_pp.completed:
            return True
        if len(self.points_pq):
            self.current_pp = self.points_pq.pop()
            return True
        else:
            return False

    def go_one_step(self):
        self.a_star_steps(self.current_pp)

    def save_to_csv(self, filename):
        np.savetxt(filename + '.csv', self.board.astype('int'), delimiter=",", fmt='%d')

    def find_paths(self):
        while self.set_pp():
            self.a_star()

    def load_file(self, filepath):
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

    def get_neighbours(self, X):
        vert = [X[0], X[0] - 1, X[0] + 1]
        horz = [X[1], X[1] - 1, X[1] + 1]
        steps = []
        for point in itertools.product(vert, horz):
            if not np.any(np.array(point) < 0) \
                    and not np.any(np.array(point) >= self.board.shape) \
                    and not np.array_equal(point, X):
                steps.append(point)
        return steps

    def get_orthogonal_neighbours(self, X):
        ns = [
            point for point in
            [(X[0] - 1, X[1]), (X[0] + 1, X[1]), (X[0], X[1] - 1), (X[0], X[1] + 1)]
            if not np.any(np.array(point) < 0) \
               and not np.any(np.array(point) >= self.board.shape)
        ]
        return ns

    def is_valid(self, point, path, tried_pins):
        # 1. Check that it is in the board
        if np.any(np.array(point) < 0) or np.any(np.array(point) >= self.board.shape):
            return False
        # 2. Check that a pin is not between two other orthogonally neighbouring pins
        neighbours = self.get_orthogonal_neighbours(point)
        pin_counter = 0
        for n in neighbours:
            pin_counter += self.board[n] != 0
        if pin_counter > 1:
            return False
        # 3. Check that it is not part of an existing path or near it
        if (point[0], point[1]) in self.invalid_nodes:
            return False
        # 4. Check that it is not already in tried pins
        if point in tried_pins:
            return False
        # 5. Check that it is not near a pin with another number
        neighbours = self.get_neighbours(point)
        for n in neighbours:
            point_value = self.board[n]
            if point_value != 0 and point_value != self.board[path[0]]:
                return False
        return True

    def next_steps(self, X, Y, path, tried_pins):
        vert = [X[0], X[0] - 1, X[0] + 1]
        horz = [X[1], X[1] - 1, X[1] + 1]
        steps = []
        for point in itertools.product(vert, horz):
            if self.is_valid(point, path, tried_pins) and not np.array_equal(point, X):
                new_path = path[:]
                new_path.append(point)
                steps.append(Step(point, X, Y, new_path, self.center))
        return steps

    def update_playground(self, path, value):
        self.paths.append(path)
        for c in path:
            self.invalid_nodes.add(c)
            self.board[c] = value
            for n in self.get_neighbours(c):
                self.invalid_nodes.add(n)

    def a_star(self):
        while not self.current_pp.completed:
            self.a_star_steps(self.current_pp)

    def a_star_steps(self, pp):
        self.a_star_step(pp, 0)
        self.a_star_step(pp, 1)
        if pp.completed:
            return
        x_limit = pp.path[0][-1]
        y_limit = pp.path[1][-1]
        if distance(np.array(x_limit), np.array(y_limit)) == 2:
            if x_limit[0] == y_limit[0]:
                pp.final_path = pp.path[0] + [(x_limit[0], x_limit[0] + 1), (x_limit[0], x_limit[0] + 2)] + pp.path[1]
                pp.completed = True
                self.update_playground(pp.final_path, pp.value)
            elif x_limit[1] == y_limit[1]:
                pp.final_path = pp.path[0] + [((x_limit[0] + y_limit[0]) // 2, x_limit[1])] + pp.path[1]
                pp.completed = True
                self.update_playground(pp.final_path, pp.value)
        neighbours = self.get_neighbours(pp.path[0][-1])
        if pp.path[1][-1] in neighbours:
            pp.final_path = pp.path[0] + pp.path[1][::-1]
            pp.completed = True
            self.update_playground(pp.final_path, pp.value)

    def a_star_step(self, pp, index):
        if np.array_equal(pp.current_x[index], pp.limits[(index + 1) % 2]):
            return
        pp.tried_pins[index].add((pp.current_x[index][0], pp.current_x[index][1]))
        further_steps = self.next_steps(pp.current_x[index], pp.limits[(index + 1) % 2], pp.path[index], pp.tried_pins[index])
        for step in further_steps:
            pp.pq[index].put(step)
        if pp.pq[index].qsize() == 0:
            pp.completed = True
            pp.final_path = [(pp.X[0], pp.X[1]), (pp.Y[0], pp.Y[1])]
            return
        step = pp.pq[index].get()
        pp.current_x[index] = step.coords
        pp.path[index] = step.path[:]
        if np.array_equal(pp.current_x[index], pp.limits[(index + 1) % 2]):
            pp.completed = True
            pp.final_path = pp.path[index][:]
            self.update_playground(pp.path[index], pp.value)


class Step:
    def __init__(self, coords, X, Y, path, board_center):
        self.coords = coords
        self.prev = X
        self.path = path
        self.dist = distance(np.array(X), np.array(coords))
        self.combined_dist = (
                distance(np.array(coords), np.array(Y))
                + distance(np.array(coords), np.array(X))
            # - 0.75 * distance(np.array(coords), np.array([board_center[0], board_center[1]]))
        )

    def __str__(self):
        return f'({self.coords[0]}, {self.coords[1]}), dist: {self.dist}, combined_dist: {self.combined_dist}'

    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.combined_dist < other.combined_dist


class PointPair:
    def __init__(self, X, Y, value, board_center):
        self.X = X
        self.Y = Y
        self.limits = [X, Y]
        self.value = value
        self.d = distance(X, Y)
        self.center_d = (distance(X, np.array([board_center[0], board_center[1]])) +
                         distance(Y, np.array([board_center[0], board_center[1]]))) / 2
        self.path = [[(X[0], X[1])], [(Y[0], Y[1])]]
        self.pq = [PriorityQueue(), PriorityQueue()]
        self.current_x = [X, Y]
        self.tried_pins = [set(), set()]
        self.completed = False

    def __lt__(self, other):
        """
        Prioritize the selection of pairs of points
        """
        return self.d > other.d
        # return self.d - 0.15 * self.center_d > other.d - 0.15 * other.center_d
        # other.center_d + 
        # and self.d > other.d
