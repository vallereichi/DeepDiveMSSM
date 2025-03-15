import numpy as np
from collections.abc import Callable

def gaussian(point:np.array, mu:float = 50, sigma:float = 30) -> float:
    return np.sum([-0.5 * np.log(2*np.pi*sigma**2) - (1/(2*sigma**2)) * (x - mu)**2 for x in point])

def parabola(x:float, y:float) -> float:
    return x**2 + y**2


def evaluate_objective_function(func:Callable[[np.array], float], point:np.array) -> float:
    return func(point)

