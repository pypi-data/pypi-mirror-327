from _typeshed import Incomplete
from pyspark.ml.torch.distributor import TorchDistributor as TorchDistributor
from typing import Any, Callable

class DeepspeedTorchDistributor(TorchDistributor):
    deepspeed_config: Incomplete
    cleanup_deepspeed_conf: bool
    def __init__(self, numGpus: int = 1, nnodes: int = 1, localMode: bool = True, useGpu: bool = True, deepspeedConfig: str | dict[str, Any] | None = None) -> None: ...
    def run(self, train_object: Callable | str, *args: Any, **kwargs: Any) -> Any | None: ...
