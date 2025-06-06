from typing import List
from copy import deepcopy

from genetic.gene import Gene
from constants import MUTATION_RATE

class Chromossome:
    def __init__(self,size:int):
        self._i = 0
        self._max = size
        self._genes = [Gene() for _ in range(size)]

    def set_genes(self, new_genes:List[Gene]):
        self._genes = new_genes

    def slice(self, start:int, end:int) -> List[Gene]:
        return [ deepcopy(self._genes[i]) for i in range(start, end) ]
    
    def __str__(self) -> str:
        return "[" + ", ".join([str(gene.value) for gene in self._genes]) + "]"

    @property
    def size(self) -> int:
        return self._max
    
    @property
    def genes(self) -> List[Gene]:
        return self._genes

    def mutate(self,rate:float=MUTATION_RATE):
        for gene in self._genes:
            gene.mutate(rate)
