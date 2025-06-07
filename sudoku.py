"""Main file for sudoku agent"""

import argparse
import sys
from alive_progress import alive_it

from constants import (
    DEFAULT_GENERATIONS,
    DEFAULT_POPULATION_SIZE,
    DEFAULT_OUTPUT_IMAGE,
    DEFAULT_CROSSOVER_RATE,
    DEFAULT_MUTATION_RATE, DEFAULT_K, DEFAULT_NUMBER_OF_PARENTS, DEFAULT_IMMIGRANT_RATE
)
from game.board import Board
from genetic.population import Population
from genetic.chromosome import crossover

def get_args() -> argparse.Namespace:
    """
    Parse CLI arguments.

    :return: argparse.Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=int, default=DEFAULT_POPULATION_SIZE)
    parser.add_argument("--generations", type=int, default=DEFAULT_GENERATIONS)
    parser.add_argument("--out-image", type=str, default=DEFAULT_OUTPUT_IMAGE)
    parser.add_argument("--cross-rate", type=float, default=DEFAULT_CROSSOVER_RATE)
    parser.add_argument("--mut-rate", type=float, default=DEFAULT_MUTATION_RATE)
    parser.add_argument("-k", type=int, default=DEFAULT_K)
    parser.add_argument("--parents", type=int, default=DEFAULT_NUMBER_OF_PARENTS)
    parser.add_argument("--immigration", type=float, default=DEFAULT_IMMIGRANT_RATE)
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":

    args = get_args()
    pop_size = args.population
    max_generations = args.generations
    output_image = args.out_image
    crossover_rate = args.cross_rate
    mutation_rate = args.mut_rate
    k = args.k
    number_of_parents = args.parents
    immigration_rate = args.immigration

    print("Using:")
    print(f"Population size: {pop_size}")
    print(f"Max generations: {max_generations}")
    print(f"Crossover rate: {crossover_rate}")
    print(f"Mutation rate: {mutation_rate}")
    print(f"K: {k}")
    print(f"Number of parents: {number_of_parents}")
    print(f"Immigration rate: {immigration_rate}")
    print(f"Saving chart at: {output_image}")

    history = []
    solution_ind = None
        
    print("---Starting Board---")
    starting_board = Board()
    starting_board.show()
        
    population = Population(pop_size, starting_board)
    
    for gen in alive_it(range(max_generations)):
    
        selected_individuals = population.select(k,number_of_parents)

        print(f"Best Individuals performances: {'; '.join([ f'ind{i+1}={individual.performance()}' for i,individual in enumerate(selected_individuals)])}")

        for individual in selected_individuals:
            if individual.found_solution():
                solution_ind = individual
                break

        chromosomes = [individual.chromosome for individual in selected_individuals]
        children = crossover(chromosomes, crossover_rate)
        population.new_generation(children, mutation_rate, immigration_rate)
    
    """plt.plot(list(range(len((history)))), history)
    plt.grid()
    plt.title("Progress of average duplicated values (less is better)")
    plt.xticks(rotation=45)
    plt.xlabel("generation")
    plt.ylabel("score")
    plt.savefig(output_image,bbox_inches="tight")
    plt.show()"""

    
