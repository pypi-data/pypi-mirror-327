from _typeshed import Incomplete
from pyspark.errors import PySparkRuntimeError as PySparkRuntimeError, PySparkTypeError as PySparkTypeError
from pyspark.rdd import PythonEvalType as PythonEvalType
from pyspark.sql.connect._typing import ColumnOrName as ColumnOrName
from pyspark.sql.connect.column import Column as Column
from pyspark.sql.connect.dataframe import DataFrame as DataFrame
from pyspark.sql.connect.expressions import ColumnReference as ColumnReference
from pyspark.sql.connect.plan import CommonInlineUserDefinedTableFunction as CommonInlineUserDefinedTableFunction, PythonUDTF as PythonUDTF
from pyspark.sql.connect.session import SparkSession as SparkSession
from pyspark.sql.connect.types import UnparsedDataType as UnparsedDataType
from pyspark.sql.connect.utils import check_dependencies as check_dependencies, get_python_ver as get_python_ver
from pyspark.sql.types import DataType as DataType, StructType as StructType

class UserDefinedTableFunction:
    func: Incomplete
    returnType: Incomplete
    evalType: Incomplete
    deterministic: Incomplete
    def __init__(self, func: type, returnType: StructType | str, name: str | None = None, evalType: int = ..., deterministic: bool = False) -> None: ...
    def __call__(self, *cols: ColumnOrName) -> DataFrame: ...
    def asDeterministic(self) -> UserDefinedTableFunction: ...

class UDTFRegistration:
    sparkSession: Incomplete
    def __init__(self, sparkSession: SparkSession) -> None: ...
    def register(self, name: str, f: UserDefinedTableFunction) -> UserDefinedTableFunction: ...
