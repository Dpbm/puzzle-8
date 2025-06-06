import random

from constants import MIN_VALUE_PER_CELL, MAX_VALUE_PER_CELL

class Gene:
    def __init__(self, min_range:int=MIN_VALUE_PER_CELL, max_range=MAX_VALUE_PER_CELL):
        self._min_range = min_range
        self._max_range = max_range
        self._set_value()
    
    def _set_value(self):
        self._value = random.randint(self._min_range, self._max_range)
    
    def mutate(self, rate:float):
        if random.randint(0,100) > rate*100:
            return
        self._set_value()

    @property
    def value(self) -> int:
        return self._value
