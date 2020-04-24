import numpy as np
from queue import PriorityQueue
import itertools


class Playground:
    def __init__(self, filepath):
        self.board = None
        self.center = None
        self.points_pq = []
        self.load_file(filepath)
        
        self.invalid_nodes = set()
        self.paths = []

    def find_paths(self):
        while self.points_pq:
            pp = self.points_pq.pop()
            pin_no = self.board[pp.X[0], pp.X[1]]
            print(pin_no)
            print(pp.center_d)
            path = self.a_star(pp.X, pp.Y)
            print(path)
            self.paths += path
            for c in path:
                self.invalid_nodes.add(c)
                self.board[c] = pin_no
                for n in self.get_neighbours(c):
                    self.invalid_nodes.add(n)
            np.savetxt("result-4.csv", self.board.astype('int'), delimiter=",", fmt='%d')

    def load_file(self, filepath):
        self.board = np.genfromtxt(filepath, delimiter=',', dtype='int')
        self.center = (self.board.shape[0] // 2, self.board.shape[1] // 2)
        # load coordinates of non zero values
        coordinates = np.argwhere(self.board)
        func = lambda row: self.board[row[0],row[1]]
        # sort by value at coordinates
        coordinates = coordinates[np.argsort(np.apply_along_axis(func, 1, coordinates))]

        for pair in zip(*[iter(coordinates)]*2):
            self.points_pq.append(PointPair(pair[0], pair[1], self.center))
        self.points_pq.sort()

    def get_neighbours(self, X):
        arr = np.array([X[0], X[1]])
        vert = [X[0], X[0]-1, X[0]+1]
        horz = [X[1], X[1]-1, X[1]+1]
        steps = []
        for point in itertools.product(vert, horz):
            if not np.any(np.array(point) < 0) \
                and not np.any(np.array(point) >= self.board.shape):
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
            n_value = self.board[n]
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
        arr = np.array([X[0], X[1]])
        vert = [X[0], X[0]-1, X[0]+1]
        horz = [X[1], X[1]-1, X[1]+1]
        steps = []
        for point in itertools.product(vert, horz):
            if self.is_valid(point, path, tried_pins) and not np.array_equal(point, X):
                new_path = path[:]
                new_path.append(point)
                steps.append(Step(point, X, Y, new_path, self.center))
        return steps
        
    def a_star(self, X, Y):
        pq = PriorityQueue()
        if distance(self.center, X) > distance(self.center, Y):
            X, Y = Y, X
        path = [(X[0], X[1])]
        tried_pins = set()
        while not np.array_equal(X, Y):
            tried_pins.add((X[0], X[1]))
            further_steps = self.next_steps(X, Y, path, tried_pins)
            # if not further_steps:
            #     break
            for step in further_steps:
                pq.put(step)
            if pq.qsize() == 0:
                break
            step = pq.get()
            X = step.coords
            path = step.path[:]
        return path

    
class Step:
    def __init__(self, coords, X, Y, path, board_center):
        self.coords = coords
        self.prev = X
        self.path = path
        self.dist = distance(np.array(X), np.array(coords))
        self.combined_dist = 0.40 * distance(np.array(coords), np.array(Y)) + 0.30 * distance(np.array(coords), np.array(X)) + 0.30 * distance(np.array(coords), np.array([board_center[0], board_center[1]]))

    def __str__(self):
        return f'({self.coords[0]}, {self.coords[1]}), dist: {self.dist}, combined_dist: {self.combined_dist}'

    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.combined_dist < other.combined_dist


class PointPair:
    def __init__(self, X, Y, board_center):
        self.X = X
        self.Y = Y
        self.d = distance(X, Y)
        self.center_d = min(distance(X, np.array([board_center[0], board_center[1]])), 
                        distance(Y, np.array([board_center[0], board_center[1]])))
    
    def __lt__(self, other):
        return self.center_d + self.d > other.center_d + other.d
        #  and self.d > other.d
    

def distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))


if __name__ == '__main__':

    filepath = 'E:\\UBB\\Semester 6\\Stratec\\2020_Internship_Challenge_Software\\Step_Two-Z.csv'

    playground = Playground(filepath)
    playground.find_paths()

    print('Finished')

    from printing_tools import print_pretty_table
    print_pretty_table(playground.board, playground.paths)
