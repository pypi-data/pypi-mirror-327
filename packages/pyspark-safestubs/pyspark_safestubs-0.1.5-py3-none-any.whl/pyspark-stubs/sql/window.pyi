from typing import Generic, TypeVar, Union
from typing_extensions import LiteralString

from py4j.java_gateway import JavaObject
from pyspark.sql._typing import ColumnOrName

TIn = TypeVar("TIn", bound=LiteralString, contravariant=True)
TIn2 = TypeVar("TIn2", bound=LiteralString)
__all__ = ['Window', 'WindowSpec']

class Window():
    unboundedPreceding: int
    unboundedFollowing: int
    currentRow: int
    @staticmethod
    def partitionBy(*cols: ColumnOrName[TIn, TIn] ) -> WindowSpec[TIn]: ...
    @staticmethod
    def orderBy(*cols: ColumnOrName[TIn, TIn] ) -> WindowSpec[TIn]: ...

class WindowSpec(Generic[TIn]):
    def __init__(self, jspec: JavaObject) -> None: ...
    def partitionBy(self, *cols: ColumnOrName[TIn2, TIn2] ) -> WindowSpec[Union[TIn, TIn2]]: ...
    def orderBy(self, *cols: ColumnOrName[TIn2, TIn2] ) -> WindowSpec[Union[TIn, TIn2]]: ...
    def rowsBetween(self, start: int, end: int) -> WindowSpec[TIn]: ...
    def rangeBetween(self, start: int, end: int) -> WindowSpec[TIn]: ...
