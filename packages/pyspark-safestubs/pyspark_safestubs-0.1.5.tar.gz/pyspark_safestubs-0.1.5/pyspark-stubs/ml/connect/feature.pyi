import numpy as np
from _typeshed import Incomplete
from pyspark import keyword_only as keyword_only
from pyspark.ml.connect.base import Estimator as Estimator, Model as Model
from pyspark.ml.connect.io_utils import CoreModelReadWrite as CoreModelReadWrite, ParamsReadWrite as ParamsReadWrite
from pyspark.ml.connect.summarizer import summarize_dataframe as summarize_dataframe
from pyspark.ml.param.shared import HasInputCol as HasInputCol, HasOutputCol as HasOutputCol
from pyspark.sql import DataFrame as DataFrame

class MaxAbsScaler(Estimator, HasInputCol, HasOutputCol, ParamsReadWrite):
    def __init__(self, *, inputCol: str | None = None, outputCol: str | None = None) -> None: ...

class MaxAbsScalerModel(Model, HasInputCol, HasOutputCol, ParamsReadWrite, CoreModelReadWrite):
    max_abs_values: Incomplete
    scale_values: Incomplete
    n_samples_seen: Incomplete
    def __init__(self, max_abs_values: np.ndarray | None = None, n_samples_seen: int | None = None) -> None: ...

class StandardScaler(Estimator, HasInputCol, HasOutputCol, ParamsReadWrite):
    def __init__(self, inputCol: str | None = None, outputCol: str | None = None) -> None: ...

class StandardScalerModel(Model, HasInputCol, HasOutputCol, ParamsReadWrite, CoreModelReadWrite):
    mean_values: Incomplete
    std_values: Incomplete
    scale_values: Incomplete
    n_samples_seen: Incomplete
    def __init__(self, mean_values: np.ndarray | None = None, std_values: np.ndarray | None = None, n_samples_seen: int | None = None) -> None: ...
