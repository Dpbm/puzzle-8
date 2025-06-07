"""
Handle individual data.
"""

from game.board import Board
from genetic.chromosome import Chromosome

class Individual:
    """
    This class holds everything an individual can do,
    from setting up its data to retrieving its own performance
    measurement.
    """
    def __init__(self, board:Board):
        self._board = board
        self._worst_fitness = (board.n**2) * 3
        self._chromosome = Chromosome(board.total_empty)

    def set_chromosome(self, chromosome:Chromosome):
        """Define the individual's chromosome"""
        self._chromosome = chromosome

    def setup_board(self):
        """
        Get the current board by applying the genes values to
        empty positions.
        """
        self._board.setup_solution_board(self._chromosome.genes)

    def performance(self) -> int:
        """
        Based on its board, check how many duplicated numbers are there.
        """
        self.setup_board()
        return self._board.total_duplicated_values()

    @property
    def board(self)  -> Board:
        """Returns the current board."""
        return self._board

    @property
    def chromosome(self) -> Chromosome:
        """Get the Individual's chromosome."""
        return self._chromosome
    
    def found_solution(self) -> bool:
        """
        Check if the individual's genes set a
        solution for the board.

        In this case, the solution is found when there are no duplicated numbers
        on rows, columns and squares.
        """

        return self._board.total_duplicated_values() == 0