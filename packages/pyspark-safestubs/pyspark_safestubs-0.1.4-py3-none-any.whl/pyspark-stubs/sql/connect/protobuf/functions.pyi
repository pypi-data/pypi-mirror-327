from pyspark.sql.connect._typing import ColumnOrName as ColumnOrName
from pyspark.sql.connect.column import Column as Column
from pyspark.sql.connect.functions import lit as lit
from pyspark.sql.connect.utils import check_dependencies as check_dependencies

def from_protobuf(data: ColumnOrName, messageName: str, descFilePath: str | None = None, options: dict[str, str] | None = None, binaryDescriptorSet: bytes | None = None) -> Column: ...
def to_protobuf(data: ColumnOrName, messageName: str, descFilePath: str | None = None, options: dict[str, str] | None = None, binaryDescriptorSet: bytes | None = None) -> Column: ...
