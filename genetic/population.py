from copy import deepcopy
import random


from game.board import Board
from genetic.individual import Individual
from genetic.chromossome import Chromossome

class Population:
    def __init__(self, amount:int, board:Board):
        self._total_individuals = amount
        self._individuals = [Individual(deepcopy(board)) for _ in range(amount)]

    def select(self):
        performances = []
        for individual in self._individuals:
            performances.append(individual.performance())

        best_individual_index = performances.index(min(performances))
        performances[best_individual_index] = 1_000_000
        second_best_individual_index = performances.index(min(performances))

        best_individual = self._individuals[best_individual_index]
        second_best_individual = self._individuals[second_best_individual_index]

        avg_performance = sum(performances)/self._total_individuals

        return best_individual,second_best_individual, avg_performance

    def crossover(self, ind1:Chromossome, ind2:Chromossome) -> Chromossome:
        ch_size = ind1.size
        percentage = random.uniform(0,0.9)
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