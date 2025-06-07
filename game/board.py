import random
from math import sqrt
from typing import List, Tuple
import numpy as np

from constants import MIN_VALUE_PER_CELL, MAX_RANDOM_PER_ROW, MAX_VALUE_PER_CELL,DEFAULT_BOARD_SIZE

Row = np.array
Column = np.array
Square = np.array
BoardData = np.array
Coordinates = Tuple[int, int]

class Board:
    def __init__(self, n:int=DEFAULT_BOARD_SIZE):
        self._n = n
        self._side = sqrt(self._n)
        self._board = np.zeros(shape=(self._n, self._n), dtype=np.uint8)
        self._empty_positions = []
        self._randomize_board()
        self._save_empty_pos()

    def _get_column(self, j:int) -> Column:
        return self._board[:, j]
    
    def _get_row(self, i:int) -> Row:
        return self._board[i]

    def _get_random_number(self,min_val:int=MIN_VALUE_PER_CELL, max_val:int=MAX_VALUE_PER_CELL) -> int:
        return random.randint(min_val,max_val)

    def _should_add_random_number(self) -> bool: return bool(random.randint(0,1))

    def _get_square_pos(self, i:int) -> int:
        return i//self._side

    def set_at_pos(self,i:int, j:int, value:int):
        self._board[i,j] = value

    def _is_in_the_same_square(self, base:Coordinates, current:Coordinates) -> bool:
        base_i, base_j = base
        current_i, current_j = current

        return self._get_square_pos(base_i) == self._get_square_pos(current_i) and self._get_square_pos(base_j) == self._get_square_pos(current_j)

    def _get_min_square(self, i:int, j:int) -> Square:
        values = []
        for row in range(self._n):
            for column in range(self._n):
                if(self._is_in_the_same_square((i,j),(row,column))):
                    values.append(self._board[row, column])
        return np.array(values, dtype=np.uint8)

    def _get_nth_square(self, n:int) -> Square:
        values = []
        for row in range(self._n):
            for column in range(self._n):
                if(self._get_square_pos(row) == n and self._get_square_pos(column) == n):
                    values.append(self._board[row, column])
        return np.array(values, dtype=np.uint8)

    def _randomize_board(self):
        self._board = np.array([
            [8, 0, 6, 0, 0, 0, 1, 0, 7],
            [0, 0, 0, 6, 0, 2, 0, 0, 0],
            [0, 5, 3, 0, 0, 4, 8, 0, 6],
            [7, 0, 4, 8, 0, 0, 6, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 9, 0],
            [1, 0, 0, 5, 0, 0, 4, 0, 0],
            [0, 0, 1, 2, 0, 0, 7, 0, 9],
            [2, 0, 0, 0, 9, 6, 0, 0, 0],
            [0, 7, 0, 0, 1, 0, 0, 8, 0],
        ], dtype=np.uint8)
        return
        for row in range(self._n):
            total_in_row = 0
            for column in range(self._n):
                get_random_number = self._should_add_random_number()

                if total_in_row >= MAX_RANDOM_PER_ROW:
                    break

                if not get_random_number:
                    continue

                column_values = self._get_column(column)
                row_values = self._get_row(row)
                square_values = self._get_min_square(row, column)

                while True:
                    random_number = self._get_random_number()
                    is_a_valid_movement = not random_number in np.concatenate((column_values, row_values, square_values), axis=None)
                    if (is_a_valid_movement):
                        self.set_at_pos(row, column, random_number)
                        break
                total_in_row += 1

    def total_duplicated_values(self):
        total = 0
        for i in range(self._n):
            total += self._n - len(np.unique(self._get_row(i)))
            total += self._n - len(np.unique(self._get_column(i)))
            total += self._n - len(np.unique(self._get_nth_square(i)))
        return total
    
    def setup_solution_board(self,values):
        for value,pos in zip(values, self._empty_positions):
            i,j = pos
            self.set_at_pos(i,j,value)

    @property
    def board(self) -> BoardData:
        return self._board

    @property
    def total_empty(self) -> int:
        return len(self._empty_positions)

    @property
    def empty_positions(self) -> List[Coordinates]:
        return self._empty_positions

    def _save_empty_pos(self):
        for i in range(self._n):
            for j in range(self._n):
                if(self._board[i][j] == 0):
                    self._empty_positions.append((i,j))
    
    @property
    def n(self) -> int:
        return self._n

    def show(self):
        print(" " + "-"*28) 
        for i in range(self._n):
            for j in range(self._n):
                if j%self._side == 0:
                    print(" | ",end="")
                print(self._board[i][j], end=" ")

            print(" | ")
            if i > 0 and (i+1) % self._side == 0 :
                print(" " + "-"*28) 
