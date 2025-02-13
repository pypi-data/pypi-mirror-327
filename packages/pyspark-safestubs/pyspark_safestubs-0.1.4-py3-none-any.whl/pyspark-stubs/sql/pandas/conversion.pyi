from py4j.java_gateway import JavaObject as JavaObject
from pyspark.errors import PySparkTypeError as PySparkTypeError
from pyspark.errors.exceptions.captured import unwrap_spark_exception as unwrap_spark_exception
from pyspark.sql import DataFrame as DataFrame
from pyspark.sql.pandas._typing import DataFrameLike as PandasDataFrameLike
from pyspark.sql.pandas.serializers import ArrowCollectSerializer as ArrowCollectSerializer
from pyspark.sql.types import ArrayType as ArrayType, DataType as DataType, MapType as MapType, StructType as StructType, TimestampType as TimestampType
from pyspark.sql.utils import is_timestamp_ntz_preferred as is_timestamp_ntz_preferred
from pyspark.traceback_utils import SCCallSiteSync as SCCallSiteSync
from typing import overload

class PandasConversionMixin:
    def toPandas(self) -> PandasDataFrameLike: ...

class SparkConversionMixin:
    @overload
    def createDataFrame(self, data: PandasDataFrameLike, samplingRatio: float | None = ...) -> DataFrame: ...
    @overload
    def createDataFrame(self, data: PandasDataFrameLike, schema: StructType | str, verifySchema: bool = ...) -> DataFrame: ...
