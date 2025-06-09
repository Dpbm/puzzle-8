"""Main file for sudoku agent"""
from typing import Tuple
import argparse
import sys
import random
from itertools import permutations
from copy import deepcopy
from time import sleep

from alive_progress import alive_it

from constants import DEFAULT_MAX_ITERATIONS, DEFAULT_MAX_RANDOM_PER_ROW
from game.board import Board

def get_args() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iter", type=int, default=DEFAULT_MAX_ITERATIONS)
    parser.add_argument("--max-random", type=int, default=DEFAULT_MAX_RANDOM_PER_ROW)
    return parser.parse_args(sys.argv[1:])

def fill_board_at_random(board:Board):
    board_grid = board.board

    all_possible_values = set(list(range(1,10)))

    for i,row in enumerate(board_grid):
        for j,val in enumerate(row):

            values_to_choose = list(all_possible_values.difference(set(row)) - {0})

            if val == 0:
                board.set_at_pos(i,j,random.choice(values_to_choose))

def get_row_values(board:Board,row_index:int):
    row = board.get_row(row_index)
    empty_positions = board.empty_positions

    values = []
    indexes = []
    for j in range(9):
        if not (row_index,j) in empty_positions:
            continue
        values.append(row[j])
        indexes.append(j)

    return values,indexes


def set_permutation(board,perm,indexes,row_index):
    i = 0
    for j in range(9):
        if j not in indexes:
            continue
        board.set_at_pos(row_index,j,perm[i])
        i += 1



def search(board:Board):
    rows_data = { i:get_row_values(board,i) for i in range(9) }
    rows_permutations = { i:list(permutations(rows_data[i][0],len(rows_data[i][0]))) for i in range(9)}

    board_performance = 1_000_000
    i = 0

    while board_performance > 0 and i < 1_000_000:
        print(i,board_performance)
        for row in range(0,9):
            performances = []
            for permutation in rows_permutations[row]:
                set_permutation(board, permutation, rows_data[row][1], row)
                performances.append(board.total_duplicated_values())
            
            best_performance = min(performances)
            best_permutation_index = performances.index(best_performance)
            set_permutation(board, rows_permutations[row][best_permutation_index], rows_data[row][1], row)
        
        new_board_performance = board.total_duplicated_values()

        if new_board_performance == board_performance:
            random_row = random.randint(0,8)
            random_perm = random.randint(0,len(rows_permutations[random_row])-1)
            set_permutation(board, rows_permutations[random_row][random_perm], rows_data[random_row][1], random_row)
            board_performance = board.total_duplicated_values()
        else:
            board_performance = new_board_performance

        # board.show()
        # sleep(0.4)


        i += 1

if __name__ == "__main__":

    args = get_args()
    max_iter = args.max_iter
    random_per_row = args.max_random

    print("Using:")
    print(f"max iterations: {max_iter}")

    history = []
        
    print("---Starting Board---")
    starting_board = Board()
    starting_board.randomize_board(random_per_row)
    starting_board.show()
    fill_board_at_random(starting_board)    
    search(starting_board)

    starting_board.show() 
    
    # for _ in alive_it(range(max_iter)):


    



    
