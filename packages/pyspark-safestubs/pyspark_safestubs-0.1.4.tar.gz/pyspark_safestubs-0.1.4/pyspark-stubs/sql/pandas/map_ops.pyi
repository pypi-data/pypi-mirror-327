from pyspark.rdd import PythonEvalType as PythonEvalType
from pyspark.sql.dataframe import DataFrame as DataFrame
from pyspark.sql.pandas._typing import ArrowMapIterFunction as ArrowMapIterFunction, PandasMapIterFunction as PandasMapIterFunction
from pyspark.sql.types import StructType as StructType

class PandasMapOpsMixin:
    def mapInPandas(self, func: PandasMapIterFunction, schema: StructType | str, barrier: bool = False) -> DataFrame: ...
    def mapInArrow(self, func: ArrowMapIterFunction, schema: StructType | str, barrier: bool = False) -> DataFrame: ...
