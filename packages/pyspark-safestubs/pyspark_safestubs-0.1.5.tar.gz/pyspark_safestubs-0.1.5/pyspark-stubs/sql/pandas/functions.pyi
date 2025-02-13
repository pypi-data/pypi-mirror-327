from _typeshed import Incomplete
from pyspark.errors import PySparkTypeError as PySparkTypeError, PySparkValueError as PySparkValueError
from pyspark.rdd import PythonEvalType as PythonEvalType
from pyspark.sql.pandas.typehints import infer_eval_type as infer_eval_type
from pyspark.sql.pandas.utils import require_minimum_pandas_version as require_minimum_pandas_version, require_minimum_pyarrow_version as require_minimum_pyarrow_version
from pyspark.sql.types import DataType as DataType
from pyspark.sql.utils import is_remote as is_remote

class PandasUDFType:
    SCALAR: Incomplete
    SCALAR_ITER: Incomplete
    GROUPED_MAP: Incomplete
    GROUPED_AGG: Incomplete

def pandas_udf(f: Incomplete | None = None, returnType: Incomplete | None = None, functionType: Incomplete | None = None): ...
