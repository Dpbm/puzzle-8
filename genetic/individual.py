from game.board import Board
from genetic.chromossome import Chromossome

class Individual:
    def __init__(self, board:Board):
        self._board = board
        self._ch = Chromossome(board.total_empty)

    def set_chromossome(self, chromossome:Chromossome):
        self._ch = chromossome

    def setup_board(self):
        self._board.setup_solution_board([
            gene.value for gene in self._ch.genes
        ])

    def performance(self) -> int:
        self.setup_board()
        return self._board.total_duplicated_values()

    @property
    def board(self)  -> Board:
        return self._board

    @property
    def chromossome(self) ->Chromossome:
        return self._ch
    
    def found_solution(self) -> bool:
        return self._board.total_duplicated_values() == 0