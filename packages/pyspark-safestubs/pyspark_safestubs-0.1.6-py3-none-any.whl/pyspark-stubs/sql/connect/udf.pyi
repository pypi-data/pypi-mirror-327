from _typeshed import Incomplete
from pyspark.errors import PySparkRuntimeError as PySparkRuntimeError, PySparkTypeError as PySparkTypeError
from pyspark.rdd import PythonEvalType as PythonEvalType
from pyspark.sql.connect._typing import ColumnOrName as ColumnOrName, DataTypeOrString as DataTypeOrString, UserDefinedFunctionLike as UserDefinedFunctionLike
from pyspark.sql.connect.column import Column as Column
from pyspark.sql.connect.expressions import ColumnReference as ColumnReference, CommonInlineUserDefinedFunction as CommonInlineUserDefinedFunction, PythonUDF as PythonUDF
from pyspark.sql.connect.session import SparkSession as SparkSession
from pyspark.sql.connect.types import UnparsedDataType as UnparsedDataType
from pyspark.sql.connect.utils import check_dependencies as check_dependencies
from pyspark.sql.types import DataType as DataType, StringType as StringType
from typing import Any, Callable

class UserDefinedFunction:
    func: Incomplete
    returnType: Incomplete
    evalType: Incomplete
    deterministic: Incomplete
    def __init__(self, func: Callable[..., Any], returnType: DataTypeOrString = ..., name: str | None = None, evalType: int = ..., deterministic: bool = True) -> None: ...
    def __call__(self, *cols: ColumnOrName) -> Column: ...
    def asNondeterministic(self) -> UserDefinedFunction: ...

class UDFRegistration:
    sparkSession: Incomplete
    def __init__(self, sparkSession: SparkSession) -> None: ...
    def register(self, name: str, f: Callable[..., Any] | UserDefinedFunctionLike, returnType: DataTypeOrString | None = None) -> UserDefinedFunctionLike: ...
    def registerJavaFunction(self, name: str, javaClassName: str, returnType: DataTypeOrString | None = None) -> None: ...
    def registerJavaUDAF(self, name: str, javaClassName: str) -> None: ...
