"""Handle Population."""

from typing import List
from copy import deepcopy
import random

from game.board import Board
from genetic.individual import Individual
from genetic.chromosome import Chromosome

SelectedIndividuals = List[Individual]
TournamentSelected = List[Individual]
Children = List[Chromosome]

class Population:
    """
    Setup methods for managing and evolving
    the population.
    """
    def __init__(self, amount:int, board:Board):
        self._total_individuals = amount
        self._individuals = [Individual(deepcopy(board)) for _ in range(amount)]

    @staticmethod
    def run_tournament(selected_individuals:TournamentSelected) -> Individual:
        """
        Run the tournament between some selected individuals
        and get the one who performed better.
        """
        performances = [individual.performance() for individual in selected_individuals]
        best_performance = min(performances)
        best_individual_index = performances.index(best_performance)
        return selected_individuals[best_individual_index]

    def _generate_tournament(self, k:int, n:int) -> List[TournamentSelected]:
        """
        Return a list of tournaments to be done.
        """


        # TODO: We could add a safeguard here, to ensure
        # the amount of available_to_select individuals never runs out of
        # to be chosen based on `n`. But for now, it's good
        available_to_select = list(range(self._total_individuals))
        tournaments = []

        for i in range(n):
            selected = random.sample(available_to_select, k)
            available_to_select = list(set(available_to_select).difference(selected))
            tournaments.append([self._individuals[index] for index in selected])

        return tournaments

    def select(self, k:int, number_of_parents:int) -> SelectedIndividuals:
        """
        Select best individuals based on a tournament.
        """
        tournaments = self._generate_tournament(k,number_of_parents)
        best_individuals = [ Population.run_tournament(tournament) for tournament in tournaments ]

        return best_individuals

    
    def new_generation(self, children:Children, mutation_rate:float, immigration_rate:float):
        """
        Restart population with new individuals (chromosomes actually)
        """

        # TODO: it's a good idea to check the amount of children
        # but for this test it's OK to let as it is right now

        #for i,child in enumerate(children):
            #self._individuals[i].set_chromosome(deepcopy(child))

        for ind in self._individuals:

            if random.random() > immigration_rate:
                # add a random new individual
                continue

            chosen_chromosome = deepcopy(random.choice(children))
            chosen_chromosome.mutate(mutation_rate)
            ind.set_chromosome(chosen_chromosome)

    def show(self):
       for ind in self._individuals:
            print(ind.chromosome)
