from alive_progress import alive_it
import matplotlib.pyplot as plt

from game.board import Board
from genetic.population import Population

if __name__ == "__main__":
    pop_size = 1000
    max_generations = 1000

    history = []
    solution_ind = None
        
    print("---Starting Board---")
    starting_board = Board()
    starting_board.show()
        
    population = Population(pop_size, starting_board)
    
    for gen in alive_it(range(max_generations), ):

        ind1, ind2, avg_performance = population.select()
        history.append(avg_performance)
        
        print("Best board: ")
        ind1.board.show()

        if(ind1.found_solution()):
            solution_ind = ind1
            break

        if(ind2.found_solution()):
            solution_ind = ind2
            break
        

        chromossome = population.crossover(ind1.chromossome, ind2.chromossome)
        population.new_generation(chromossome)

    plt.plot(list(range(len((history)))), history)
    plt.grid()
    plt.title("Progress of average duplicated values (less is better)")
    plt.xticks(rotation=45)
    plt.xlabel("generation")
    plt.ylabel("score")
    plt.savefig("result.png",bbox_inches="tight")

    