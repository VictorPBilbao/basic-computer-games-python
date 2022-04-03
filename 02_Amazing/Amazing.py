import random
from collections import deque
from enum import Enum

class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Cell(Enum):
    V_WALL = '|'
    H_WALL = '-'
    INTERSECTION = '+'
    ISLAND = 'o'
    DELETED = " "

class Maze():
    def __init__(self, m: int, n: int) -> None:
        self.m = m
        self.n = n
        
        #* count for additional walls and intersections
        self.rows = 2 * m + 1
        self.cols = 2 * n + 1
        
        #* create each line of the maze, they will alternate in the beginning
        self.line_no_island = [*[Cell.INTERSECTION, Cell.H_WALL]
                               * (self.n)] + [Cell.INTERSECTION]
        self.line_island = [*[Cell.V_WALL, Cell.ISLAND]
                            * (self.n)] + [Cell.V_WALL]
        
        self.generate_maze()
        self.set_entrances()
        self.build_path()
    
    def generate_maze(self) -> None:
        self.maze_array = []
        for i in range(self.rows):
            if i % 2 == 0:
                self.maze_array.append(self.line_no_island.copy())
            else:
                self.maze_array.append(self.line_island.copy())
    
    def set_entrances(self) -> None:
        #* Pick a random entrance and set it as start cell ( bottom of the matrix )
        self.start = (self.rows - 2, random.choice(range(1, self.cols, 2)))
        self.end = (1, random.choice(range(1, self.cols, 2)))
        
        #* mark start cell and bottom wall as used
        self.maze_array[self.start[0]][self.start[1]] = Cell.DELETED
        self.maze_array[self.start[0] + 1][self.start[1]] = Cell.DELETED
        
        #* delete random horizontal wall at th end ( top of the matrix )
        self.maze_array[0][self.end[1]] = Cell.DELETED
    
    def __str__(self) -> str:
        return "".join(
            ''.join(map(lambda x: x.value, i)) + '\n' for i in self.maze_array
        )
    
    def check_cell_possible_directions(self, i: int, j: int) -> list[Directions]:
        #* check unused islands that wew can go to and return d=the directions
        possible_directions = []
        if i > 1 and self.maze_array[i - 2][j] == Cell.ISLAND:
            possible_directions.append(Directions.UP)
        if i < self.rows - 2 and self.maze_array[i + 2][j] == Cell.ISLAND:
            possible_directions.append(Directions.DOWN)
        if j > 1 and self.maze_array[i][j - 2] == Cell.ISLAND:
            possible_directions.append(Directions.LEFT)
        if j < self.cols - 2 and self.maze_array[i][j + 2] == Cell.ISLAND:
            possible_directions.append(Directions.RIGHT)
        return possible_directions
    
    def build_path(self) -> None:
        #* maze generating algorithm, go to random directions and if we cant go more go back until no more islands
        cur_position = self.start
        path = deque()
        path.append(cur_position)
        while len(path) > 0:
            directions = self.check_cell_possible_directions(*cur_position)
            if len(directions) == 0:
                cur_position = path.pop()
                continue
            choice = random.choice(directions)
            cur_position = self.goto(*cur_position, choice)
            path.append(cur_position)
            self.maze_array[cur_position[0]][cur_position[1]] = Cell.DELETED
            
    def goto(self, i: int, j: int, direction: Directions) -> tuple:
        #* jump from one island to the next random one
        self.maze_array[i][j] = Cell.DELETED
        if direction == Directions.UP:
            self.maze_array[i - 1][j] = Cell.DELETED
            return (i - 2, j)
        elif direction == Directions.DOWN:
            self.maze_array[i + 1][j] = Cell.DELETED
            return (i + 2, j)
        elif direction == Directions.LEFT:
            self.maze_array[i][j - 1] = Cell.DELETED
            return (i, j - 2)
        elif direction == Directions.RIGHT:
            self.maze_array[i][j + 1] = Cell.DELETED
            return (i, j + 2)

def main():
    print(" " * 28 + "AMAZING PROGRAM")
    print(" " * 15 + "CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY\n\n\n")
    while True:
        dimensions = list(map(int, input("Enter the dimensions of the maze (m, n): ").split(',')))
        if dimensions[0] >= 2 and dimensions[1] >= 2:
            break
        print("Dimensions must greater than 1")
    
    print(Maze(*dimensions))

if __name__ == '__main__':
    main()