from _typeshed import Incomplete
from pyspark import keyword_only as keyword_only
from pyspark.ml.common import inherit_doc as inherit_doc
from pyspark.ml.connect.base import PredictionModel as PredictionModel, Predictor as Predictor, _PredictorParams
from pyspark.ml.connect.io_utils import CoreModelReadWrite as CoreModelReadWrite, ParamsReadWrite as ParamsReadWrite
from pyspark.ml.param.shared import HasBatchSize as HasBatchSize, HasFitIntercept as HasFitIntercept, HasLearningRate as HasLearningRate, HasMaxIter as HasMaxIter, HasMomentum as HasMomentum, HasNumTrainWorkers as HasNumTrainWorkers, HasProbabilityCol as HasProbabilityCol, HasSeed as HasSeed, HasTol as HasTol, HasWeightCol as HasWeightCol
from pyspark.ml.torch.distributor import TorchDistributor as TorchDistributor
from pyspark.sql import DataFrame as DataFrame
from pyspark.sql.functions import count as count, countDistinct as countDistinct, lit as lit
from typing import Any

class _LogisticRegressionParams(_PredictorParams, HasMaxIter, HasFitIntercept, HasTol, HasWeightCol, HasNumTrainWorkers, HasBatchSize, HasLearningRate, HasMomentum, HasProbabilityCol, HasSeed):
    def __init__(self, *args: Any) -> None: ...

class LogisticRegression(Predictor['LogisticRegressionModel'], _LogisticRegressionParams, ParamsReadWrite):
    def __init__(self, *, featuresCol: str = 'features', labelCol: str = 'label', predictionCol: str = 'prediction', probabilityCol: str = 'probability', maxIter: int = 100, tol: float = 1e-06, numTrainWorkers: int = 1, batchSize: int = 32, learningRate: float = 0.001, momentum: float = 0.9, seed: int = 0) -> None: ...

class LogisticRegressionModel(PredictionModel, _LogisticRegressionParams, ParamsReadWrite, CoreModelReadWrite):
    torch_model: Incomplete
    num_features: Incomplete
    num_classes: Incomplete
    def __init__(self, torch_model: Any = None, num_features: int | None = None, num_classes: int | None = None) -> None: ...
    @property
    def numFeatures(self) -> int: ...
    @property
    def numClasses(self) -> int: ...
