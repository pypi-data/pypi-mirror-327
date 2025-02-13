import pandas as pd
from pyspark import cloudpickle as cloudpickle
from pyspark.sql import DataFrame as DataFrame
from pyspark.sql.functions import col as col, pandas_udf as pandas_udf
from typing import Any, Callable

def aggregate_dataframe(dataframe: DataFrame | pd.DataFrame, input_col_names: list[str], local_agg_fn: Callable[[pd.DataFrame], Any], merge_agg_state: Callable[[Any, Any], Any], agg_state_to_result: Callable[[Any], Any]) -> Any: ...
def transform_dataframe_column(dataframe: DataFrame | pd.DataFrame, input_cols: list[str], transform_fn: Callable[..., Any], output_cols: list[tuple[str, str]]) -> DataFrame | pd.DataFrame: ...
