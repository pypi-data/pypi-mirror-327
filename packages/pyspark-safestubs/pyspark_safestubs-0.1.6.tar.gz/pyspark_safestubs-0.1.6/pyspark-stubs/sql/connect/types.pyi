import pyspark.sql.connect.proto as pb2
from _typeshed import Incomplete
from pyspark.errors import PySparkAssertionError as PySparkAssertionError
from pyspark.sql.connect.utils import check_dependencies as check_dependencies
from pyspark.sql.types import ArrayType as ArrayType, BinaryType as BinaryType, BooleanType as BooleanType, ByteType as ByteType, CharType as CharType, DataType as DataType, DateType as DateType, DayTimeIntervalType as DayTimeIntervalType, DecimalType as DecimalType, DoubleType as DoubleType, FloatType as FloatType, IntegerType as IntegerType, LongType as LongType, MapType as MapType, NullType as NullType, ShortType as ShortType, StringType as StringType, StructField as StructField, StructType as StructType, TimestampNTZType as TimestampNTZType, TimestampType as TimestampType, UserDefinedType as UserDefinedType, VarcharType as VarcharType, YearMonthIntervalType as YearMonthIntervalType
from typing import Any

JVM_BYTE_MIN: int
JVM_BYTE_MAX: int
JVM_SHORT_MIN: int
JVM_SHORT_MAX: int
JVM_INT_MIN: int
JVM_INT_MAX: int
JVM_LONG_MIN: int
JVM_LONG_MAX: int

class UnparsedDataType(DataType):
    data_type_string: Incomplete
    def __init__(self, data_type_string: str) -> None: ...
    def simpleString(self) -> str: ...
    def jsonValue(self) -> dict[str, Any]: ...
    def needConversion(self) -> bool: ...
    def toInternal(self, obj: Any) -> Any: ...
    def fromInternal(self, obj: Any) -> Any: ...

def pyspark_types_to_proto_types(data_type: DataType) -> pb2.DataType: ...
def proto_schema_to_pyspark_data_type(schema: pb2.DataType) -> DataType: ...
