"""Main file for sudoku agent"""

import argparse
import sys
from alive_progress import alive_it

from constants import (
    DEFAULT_GENERATIONS,
    DEFAULT_POPULATION_SIZE,
    DEFAULT_OUTPUT_IMAGE,
    DEFAULT_CROSSOVER_RATE,
    DEFAULT_MUTATION_RATE,
    DEFAULT_IMMIGRANT_RATE,
    DEFAULT_MAX_RANDOM_PER_ROW
)
from game.board import Board
from genetic.population import Population, new_generation
from genetic.chromosome import crossover

def get_args() -> argparse.Namespace:
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--population", type=int, default=DEFAULT_POPULATION_SIZE)
    parser.add_argument("--generations", type=int, default=DEFAULT_GENERATIONS)
    parser.add_argument("--out-image", type=str, default=DEFAULT_OUTPUT_IMAGE)
    parser.add_argument("--cross-rate", type=float, default=DEFAULT_CROSSOVER_RATE)
    parser.add_argument("--mut-rate", type=float, default=DEFAULT_MUTATION_RATE)
    parser.add_argument("--immigration", type=float, default=DEFAULT_IMMIGRANT_RATE)
    parser.add_argument("--random-per-row", type=int, default=DEFAULT_MAX_RANDOM_PER_ROW)
    return parser.parse_args(sys.argv[1:])


if __name__ == "__main__":

    args = get_args()
    pop_size = args.population
    max_generations = args.generations
    output_image = args.out_image
    crossover_rate = args.cross_rate
    mutation_rate = args.mut_rate
    immigration_rate = args.immigration
    random_per_row = args.random_per_row

    print("Using:")
    print(f"Population size: {pop_size}")
    print(f"Max generations: {max_generations}")
    print(f"Crossover rate: {crossover_rate}")
    print(f"Mutation rate: {mutation_rate}")
    print(f"Immigration rate: {immigration_rate}")
    print(f"Total Random numbers per row: {random_per_row}")
    print(f"Saving chart at: {output_image}")

    history = []
    solution_ind = None
        
    print("---Starting Board---")
    starting_board = Board()
    starting_board.randomize_board(random_per_row)
    starting_board.show()
        
    population = Population(pop_size, starting_board)
    
    for gen in alive_it(range(max_generations)):
    
        ind1,ind2 = population.select()

        ind1.board.show()
        print(f"Best Individuals performances: ind1={ind1.performance()}; ind2={ind2.performance()}")

        if ind1.found_solution():
            solution_ind = ind1
            break

        if ind2.found_solution():
            solution_ind = ind2
            break

        child1, child2 = crossover(ind1.chromosome, ind2.chromosome, crossover_rate, starting_board)
        population = new_generation(pop_size, starting_board, [child1,child2], mutation_rate, immigration_rate)


    """plt.plot(list(range(len((history)))), history)
    plt.grid()
    plt.title("Progress of average duplicated values (less is better)")
    plt.xticks(rotation=45)
    plt.xlabel("generation")
    plt.ylabel("score")
    plt.savefig(output_image,bbox_inches="tight")
    plt.show()"""

    
