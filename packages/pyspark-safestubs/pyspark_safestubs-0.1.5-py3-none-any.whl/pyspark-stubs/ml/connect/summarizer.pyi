import numpy as np
import pandas as pd
from _typeshed import Incomplete
from pyspark.ml.connect.util import aggregate_dataframe as aggregate_dataframe
from pyspark.sql import DataFrame as DataFrame
from typing import Any

class SummarizerAggState:
    min_values: Incomplete
    max_values: Incomplete
    count: int
    sum_values: Incomplete
    square_sum_values: Incomplete
    def __init__(self, input_array: np.ndarray) -> None: ...
    def update(self, input_array: np.ndarray) -> None: ...
    def merge(self, state: SummarizerAggState) -> SummarizerAggState: ...
    def to_result(self, metrics: list[str]) -> dict[str, Any]: ...

def summarize_dataframe(dataframe: DataFrame | pd.DataFrame, column: str, metrics: list[str]) -> dict[str, Any]: ...
