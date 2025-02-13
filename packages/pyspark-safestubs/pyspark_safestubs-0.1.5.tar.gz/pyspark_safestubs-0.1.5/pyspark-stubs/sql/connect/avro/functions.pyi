from pyspark.sql.connect._typing import ColumnOrName as ColumnOrName
from pyspark.sql.connect.column import Column as Column
from pyspark.sql.connect.functions import lit as lit
from pyspark.sql.connect.utils import check_dependencies as check_dependencies

def from_avro(data: ColumnOrName, jsonFormatSchema: str, options: dict[str, str] | None = None) -> Column: ...
def to_avro(data: ColumnOrName, jsonFormatSchema: str = '') -> Column: ...
