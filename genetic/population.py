from copy import deepcopy
import random
import numpy as np

from constants import DEFAULT_BOARD_SIZE
from game.board import Board
from genetic.individual import Individual
from genetic.chromossome import Chromossome

class Population:
    def __init__(self, amount:int, board:Board):
        self._total_individuals = amount
        self._worst_fitness = (DEFAULT_BOARD_SIZE**2) * 3
        self._individuals = [Individual(deepcopy(board)) for _ in range(amount)]

    def select(self):
        performances = []
        # inverse_performances = np.zeros(shape=(self._total_individuals), dtype=np.uint16)

        for i,individual in enumerate(self._individuals):
            performance = individual.performance()
            performances.append(performance)
            # inverse_performances[i] = np.abs( self._worst_fitness - performance )

        # probabilities = inverse_performances / np.sum(inverse_performances)
        # roulette = np.zeros(shape=(self._total_individuals), dtype=np.float32)
        #
        # for i,prob in enumerate(probabilities):
        #     if i == 0:
        #         roulette[i] = prob
        #         continue
        #
        #     roulette[i] = roulette[i-1]+prob
        # 
        # roulette_positions = [random.random() for _ in range(2)]
        # parents = []
        #
        # for pos in roulette_positions:
        #     for i,val in enumerate(roulette):
        #         if val < pos:
        #             continue
        #         parents.append(self._individuals[0 if i == 0 else i-1])
        #         break

        i1 = performances.index(min(performances))
        performances[i1] = 10000
        i2 = performances.index(min(performances))

        parents = [
            self._individuals[i1], self._individuals[i2]
        ]

        avg_performance = sum(performances)/self._total_individuals

        return parents[0], parents[1], avg_performance

    def crossover(self, ind1:Chromossome, ind2:Chromossome) -> Chromossome:
        ch_size = ind1.size
        # percentage = random.uniform(0.1, 0.6)
        percentage = 0.4
        cut_position = int(percentage * ch_size)

        first_part = ind1.slice(0, cut_position)
        second_part = ind2.slice(cut_position,ch_size)

        new_ch = Chromossome(ch_size)
        new_ch.set_genes([*first_part, *second_part])

        return new_ch
    
    def new_generation(self, base_chromossome:Chromossome):
        for ind in self._individuals:
            ind_chromossome = deepcopy(base_chromossome)
            ind_chromossome.mutate()
            ind.set_chromossome(ind_chromossome)
            ind.setup_board()

    def show(self):
       for ind in self._individuals:
            print(ind.chromossome)
