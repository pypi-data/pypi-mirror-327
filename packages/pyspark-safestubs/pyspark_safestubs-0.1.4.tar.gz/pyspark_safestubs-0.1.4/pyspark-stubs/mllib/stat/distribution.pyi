from pyspark.mllib.linalg import Matrix, Vector
from typing import NamedTuple

__all__ = ['MultivariateGaussian']

class MultivariateGaussian(NamedTuple):
    mu: Vector
    sigma: Matrix
