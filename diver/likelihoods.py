import numpy as np

def gaussian(point_dim:float, params:tuple[float]) -> float:
    mu = params[0]
    sigma = params[1]
    return -0.5 * np.log(2*np.pi*sigma**2) - (1/(2*sigma**2)) * (point_dim - mu)**2


def eval_likelihood(likelihood, params:tuple[float], point:np.array) -> float:
    return likelihood(point, params)


def comb_likelihood(lh_values:list[float]) -> float:
    return np.sum(lh_values)