from _typeshed import Incomplete
from pyspark.pandas.indexes.base import Index as Index
from pyspark.pandas.missing.indexes import MissingPandasLikeTimedeltaIndex as MissingPandasLikeTimedeltaIndex
from pyspark.pandas.series import Series as Series
from typing import Any

HOURS_PER_DAY: int
MINUTES_PER_HOUR: int
SECONDS_PER_MINUTE: int
MILLIS_PER_SECOND: int
MICROS_PER_MILLIS: int
SECONDS_PER_HOUR: Incomplete
SECONDS_PER_DAY: Incomplete
MICROS_PER_SECOND: Incomplete

class TimedeltaIndex(Index):
    def __new__(cls, data: Incomplete | None = None, unit: Incomplete | None = None, freq=..., closed: Incomplete | None = None, dtype: Incomplete | None = None, copy: bool = False, name: Incomplete | None = None): ...
    def __getattr__(self, item: str) -> Any: ...
    @property
    def days(self) -> Index: ...
    @property
    def seconds(self) -> Index: ...
    @property
    def microseconds(self) -> Index: ...
    def all(self, *args, **kwargs) -> None: ...
