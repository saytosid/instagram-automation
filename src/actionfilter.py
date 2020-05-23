import random
from typing import Iterable, Callable


class ProbabilisticActionFilter:
    def __init__(self, probability_success: float):
        self.probability_success = probability_success

    def __call__(self) -> bool:
        return random.random() < self.probability_success


class FilterGroup:
    def __init__(self, filters: Iterable[Callable]):
        self.filters = filters

    def __call__(self) -> bool:
        return all(f() for f in self.filters)
