from _typeshed import Incomplete
from pyspark.errors import PySparkRuntimeError as PySparkRuntimeError
from pyspark.serializers import CPickleSerializer as CPickleSerializer, UTF8Deserializer as UTF8Deserializer
from typing import IO

pickleSer: Incomplete
utf8_deserializer: Incomplete

def check_python_version(infile: IO) -> None: ...
