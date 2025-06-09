import argparse
import random
import sys
from copy import deepcopy
from alive_progress import alive_it
import matplotlib.pyplot as plt
from math import ceil

class Board:
    def __init__(self, b=None):
        self._target_positions = [
            (i,j)
            for i in range(3)
            for j in range(3)
            if i+j != 4
        ]
        self._target = [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]
                ]
        self._board = b

        if b is None:
            self._board = []
            self._generate_board()

    @property
    def board(self):
        return self._board

    @classmethod
    def new_board(cls, board_matrix):
        return cls(board_matrix)

    def _generate_board(self):
        self._board = deepcopy(self._target)

        while True:

            values = list(range(0,9))
            random.shuffle(values)
            new_board = []
            for _ in range(3):
                new_board.append([])
                for __ in range(3):
                    new_board[_].append(values.pop(0))

            self._board = new_board

            if self.is_solvable():
                break


    def show(self):
        for row in self._board:
            print(" ".join(map(str, row)))

    def empty_position(self):
        for r in range(3):
            for c in range(3):
                if self._board[r][c] == 0:
                    return r, c
        return -1, -1

    def move(self, movement):
        br, bc = self.empty_position()
        new_board = deepcopy(self._board)

        dr, dc = movement
        target_r, target_c = br + dr, bc + dc

        if 0 <= target_r < 3 and 0 <= target_c < 3:
            new_board[br][bc], new_board[target_r][target_c] = new_board[target_r][target_c], new_board[br][bc]
            return Board.new_board(new_board)
        return None

    def distance(self):
        d = 0
        for r_current in range(3):
            for c_current in range(3):
                tile = self._board[r_current][c_current]
                if tile == 0:
                    continue
                r_target, c_target = self._target_positions[tile-1]
                d += abs(r_current - r_target) + abs(c_current - c_target)
        return d

    def neighbors(self):
        neighbors = []
        moves_map = {
            (-1, 0): "Up",
            (1, 0): "Down",
            (0, -1): "Left",
            (0, 1): "Right"
        }

        for dr, dc in moves_map:
            new_board = self.move((dr, dc))
            if new_board:
                neighbors.append(new_board)
        return neighbors

    def is_solvable(self):
        flat_board = [ tile
                       for row in self._board
                       for tile in row
                       if tile != 0
                       ]

        inversions = 0
        n = len(flat_board)
        for i in range(n):
            for j in range(i + 1, n):
                if flat_board[i] > flat_board[j]:
                    inversions += 1

        return inversions % 2 == 0
    
    def plot_board(self):
        plt.axis('off')

        plt.imshow(self._board, cmap="winter")

        for row,r_val in enumerate(self._board):
            for col,c_val in enumerate(r_val):
                plt.text(col, row, str(c_val), ha='center', va='center', color='white', fontsize=14)
    
    def save_board(self,label):
        self.plot_board()
        plt.savefig(f"{label}.png",bbox_inches="tight")




class InvalidBoard(Exception):
    def __init__(self):
        self.message = "Invalid board. This board is not solvable!"
        super().__init__(self.message)

class Solver:

    @staticmethod
    def solve_hill_climbing(board,max_iter,max_restart,history):
        if not board.is_solvable():
            raise InvalidBoard()

        best_cost_overall_restarts = 1_000_000
        best_path_overall_restarts = []

        total_i = 0
        for r in range(max_restart):
            print(f"r={r}")

            current_board = deepcopy(board)
            best_cost = current_board.distance()
            path = [current_board]

            for i in alive_it(range(max_iter)):
                total_i += 1
                history.append(best_cost)

                if best_cost == 0:
                    return path

                neighbors = current_board.neighbors()
                improving_neighbors = []
                for neighbor_board in neighbors:
                    neighbor_cost = neighbor_board.distance()
                    if neighbor_cost < best_cost:
                        improving_neighbors.append((neighbor_board, neighbor_cost))

                if improving_neighbors:
                    chosen_neighbor_board, chosen_cost = random.choice(improving_neighbors)

                    current_board = deepcopy(chosen_neighbor_board)
                    best_cost = chosen_cost
                    path.append(current_board)
                else:
                    # no solution was found, try again
                    break

                print(f"i={i}; best_cost={best_cost}")
            
            if(best_cost < best_cost_overall_restarts):
                best_cost_overall_restarts = best_cost
                best_path_overall_restarts = path

        return best_path_overall_restarts



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iter", type=int, default=1_000_000)
    parser.add_argument("--max-restart", type=int, default=1000)
    args = parser.parse_args(sys.argv[1:])

    tests = [
        (
            "easy",
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 0, 8]
            ]
        ),
        (
            "medium",
            [
                [1, 2, 3],
                [0, 4, 6],
                [7, 5, 8]
            ]

        ),
        (
            "hard",
            [
                [6, 4, 7],
                [8, 5, 0],
                [3, 2, 1]
            ]
            
        )
    ]

    for label,board in tests:

        b = Board(board)
        b.save_board(label)
        plt.close('all')

        history = []
        solution = None
        try:
            solution = Solver.solve_hill_climbing(b,args.max_iter, args.max_restart,history)
        except:
            print("Failed!")


        sol_size= len(solution)
        rows = ceil(sol_size/3)
        cols = 3 if sol_size >= 3 else sol_size
        step = 0

        plt.plot(list(range(len(history))), history)
        plt.xlabel("iterations")
        plt.ylabel("cost")
        plt.title("Evolution")
        plt.savefig(f"evolution_{label}.png", bbox_inches="tight")
        plt.close('all')


        for i in range(rows):
            for j in range(cols):
                if(step > sol_size-1):
                    break

                plt.subplot(rows,cols,step+1)
                solution[step].plot_board()

                step += 1
        plt.savefig(f"solution_{label}.png",bbox_inches="tight")
        plt.close('all')


