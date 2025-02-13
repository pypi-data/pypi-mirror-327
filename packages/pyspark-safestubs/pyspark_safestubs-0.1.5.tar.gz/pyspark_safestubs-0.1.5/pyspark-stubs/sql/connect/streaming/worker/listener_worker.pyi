from _typeshed import Incomplete
from pyspark import worker as worker
from pyspark.java_gateway import local_connect_and_auth as local_connect_and_auth
from pyspark.serializers import CPickleSerializer as CPickleSerializer, UTF8Deserializer as UTF8Deserializer, read_int as read_int, write_int as write_int
from pyspark.sql import SparkSession as SparkSession
from pyspark.sql.streaming.listener import QueryIdleEvent as QueryIdleEvent, QueryProgressEvent as QueryProgressEvent, QueryStartedEvent as QueryStartedEvent, QueryTerminatedEvent as QueryTerminatedEvent
from pyspark.worker_util import check_python_version as check_python_version
from typing import IO

pickle_ser: Incomplete
utf8_deserializer: Incomplete

def main(infile: IO, outfile: IO) -> None: ...
