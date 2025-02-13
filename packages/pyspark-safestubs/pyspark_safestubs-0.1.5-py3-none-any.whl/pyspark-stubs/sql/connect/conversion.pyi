import pyarrow as pa
import pyspark.sql.connect.proto as pb2
from pyspark.sql.connect.utils import check_dependencies as check_dependencies
from pyspark.sql.pandas.types import to_arrow_schema as to_arrow_schema
from pyspark.sql.types import ArrayType as ArrayType, BinaryType as BinaryType, DataType as DataType, DecimalType as DecimalType, MapType as MapType, NullType as NullType, Row as Row, StringType as StringType, StructField as StructField, StructType as StructType, TimestampNTZType as TimestampNTZType, TimestampType as TimestampType, UserDefinedType as UserDefinedType
from pyspark.storagelevel import StorageLevel as StorageLevel
from typing import Any, Sequence

class LocalDataToArrowConversion:
    @staticmethod
    def convert(data: Sequence[Any], schema: StructType) -> pa.Table: ...

class ArrowTableToRowsConversion:
    @staticmethod
    def convert(table: pa.Table, schema: StructType) -> list[Row]: ...

def storage_level_to_proto(storage_level: StorageLevel) -> pb2.StorageLevel: ...
def proto_to_storage_level(storage_level: pb2.StorageLevel) -> StorageLevel: ...
