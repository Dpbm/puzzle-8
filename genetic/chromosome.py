"""
Handle Chromosome Data and functions.
"""

from typing import List
from itertools import combinations
from copy import deepcopy
import random

Gene = int

class Chromosome:
    """Set up a structure to manipulate a batch of genes."""

    def __init__(self,size:int):
        self._max = size
        self._genes = list(range(1,10))
        random.shuffle(self._genes)

    def set_genes(self, new_genes:List[Gene]):
        """
        Set genes from an external array.
        """
        self._genes = new_genes

    def slice(self, start:int, end:int) -> List[Gene]:
        """
        Cut Genes from a Chromosome based on a specific index range.
        """
        return [ deepcopy(self._genes[i]) for i in range(start, end) ]
    
    def __str__(self) -> str:
        """
        Show genes.
        """
        return "[" + ", ".join([str(gene) for gene in self._genes]) + "]"

    @property
    def size(self) -> int:
        """
        Total of genes.
        """
        return self._max
    
    @property
    def genes(self) -> List[Gene]:
        """
        Get the list of genes objects.
        """
        return self._genes

    def mutate(self,rate:float):
        """
        Mutate genes based on a rate.
        """
        if random.random() > rate:
            return
        random.shuffle(self._genes)


def crossover(chromosomes:List[Chromosome], rate:float) -> List[Chromosome]:
    """
    Do the crossover of two individuals' chromosomes.
    """

    # TODO: We could add a safeguard to ensure every chromosome has the same size
    # but for now it's good as it is.

    children = []
    comb = list(combinations(chromosomes,2))
    ch_size = chromosomes[0].size

    for _ in range(len(chromosomes)):
        ch1,ch2 = None,None

        while True:
            ch1, ch2 = random.choice(comb)
            if ch1 not in children or ch2 not in children:
                break

        should_cross = random.random() <= rate

        if not should_cross:
            children.append(ch1 if ch1 not in children else ch2)
            continue


        percentage_from_ind1 = random.uniform(0.1, 0.9)
        cut_point = int(ch_size * percentage_from_ind1)

        child1_chromosome = Chromosome(ch_size)
        child2_chromosome = Chromosome(ch_size)

        child1_ind1_part = ch1.slice(0, cut_point)
        child1_ind2_part = ch2.slice(cut_point, ch_size)

        child2_ind2_part = ch2.slice(0, cut_point)
        child2_ind1_part = ch1.slice(cut_point, ch_size)

        child1_chromosome.set_genes([*child1_ind1_part, *child1_ind2_part])
        child2_chromosome.set_genes([*child2_ind2_part, *child2_ind1_part])

        children.append(child1_chromosome)
        children.append(child2_chromosome)

    return children