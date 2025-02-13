import pandas as pd
import pyspark.sql.types as types
from _typeshed import Incomplete
from pyspark.pandas._typing import Dtype as Dtype, T as T
from pyspark.pandas.internal import InternalField as InternalField
from pyspark.sql.pandas.types import from_arrow_type as from_arrow_type, to_arrow_type as to_arrow_type
from typing import Any, Callable, Generic

extension_dtypes: tuple[type, ...]
extension_dtypes_available: bool
extension_object_dtypes_available: bool
extension_float_dtypes_available: bool

class SeriesType(Generic[T]):
    dtype: Incomplete
    spark_type: Incomplete
    def __init__(self, dtype: Dtype, spark_type: types.DataType) -> None: ...

class DataFrameType:
    index_fields: Incomplete
    data_fields: Incomplete
    fields: Incomplete
    def __init__(self, index_fields: list['InternalField'], data_fields: list['InternalField']) -> None: ...
    @property
    def dtypes(self) -> list[Dtype]: ...
    @property
    def spark_type(self) -> types.StructType: ...

class ScalarType:
    dtype: Incomplete
    spark_type: Incomplete
    def __init__(self, dtype: Dtype, spark_type: types.DataType) -> None: ...

class UnknownType:
    tpe: Incomplete
    def __init__(self, tpe: Any) -> None: ...

class IndexNameTypeHolder:
    name: Incomplete
    tpe: Incomplete
    short_name: str

class NameTypeHolder:
    name: Incomplete
    tpe: Incomplete
    short_name: str

def as_spark_type(tpe: str | type | Dtype, *, raise_error: bool = True, prefer_timestamp_ntz: bool = False) -> types.DataType: ...
def spark_type_to_pandas_dtype(spark_type: types.DataType, *, use_extension_dtypes: bool = False) -> Dtype: ...
def pandas_on_spark_type(tpe: str | type | Dtype) -> tuple[Dtype, types.DataType]: ...
def infer_pd_series_spark_type(pser: pd.Series, dtype: Dtype, prefer_timestamp_ntz: bool = False) -> types.DataType: ...
def infer_return_type(f: Callable) -> SeriesType | DataFrameType | ScalarType | UnknownType: ...
def create_type_for_series_type(param: Any) -> type[SeriesType]: ...
def create_tuple_for_frame_type(params: Any) -> object: ...
