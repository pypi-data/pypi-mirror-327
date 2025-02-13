import torch
from _typeshed import Incomplete
from pyspark.sql.types import StructType as StructType
from typing import Any, Iterator

class _SparkPartitionTorchDataset(torch.utils.data.IterableDataset):
    arrow_file_path: Incomplete
    num_samples: Incomplete
    field_types: Incomplete
    field_converters: Incomplete
    def __init__(self, arrow_file_path: str, schema: StructType, num_samples: int) -> None: ...
    def __iter__(self) -> Iterator[Any]: ...
