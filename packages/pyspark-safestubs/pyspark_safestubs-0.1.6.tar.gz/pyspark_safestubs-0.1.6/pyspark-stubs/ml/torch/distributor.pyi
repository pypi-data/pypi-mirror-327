from _typeshed import Incomplete
from pyspark import cloudpickle as cloudpickle
from pyspark.ml.torch.log_communication import LogStreamingClient as LogStreamingClient, LogStreamingServer as LogStreamingServer
from pyspark.resource.information import ResourceInformation as ResourceInformation
from pyspark.sql import DataFrame as DataFrame, SparkSession as SparkSession
from pyspark.taskcontext import BarrierTaskContext as BarrierTaskContext
from typing import Any, Callable

SPARK_PARTITION_ARROW_DATA_FILE: str
SPARK_DATAFRAME_SCHEMA_FILE: str

class Distributor:
    is_remote: Incomplete
    spark: Incomplete
    is_spark_local_master: bool
    logger: Incomplete
    num_processes: Incomplete
    local_mode: Incomplete
    use_gpu: Incomplete
    num_tasks: Incomplete
    ssl_conf: Incomplete
    def __init__(self, num_processes: int = 1, local_mode: bool = True, use_gpu: bool = True, ssl_conf: str | None = None) -> None: ...

class TorchDistributor(Distributor):
    input_params: Incomplete
    def __init__(self, num_processes: int = 1, local_mode: bool = True, use_gpu: bool = True, _ssl_conf: str = ...) -> None: ...
    def run(self, train_object: Callable | str, *args: Any, **kwargs: Any) -> Any | None: ...
