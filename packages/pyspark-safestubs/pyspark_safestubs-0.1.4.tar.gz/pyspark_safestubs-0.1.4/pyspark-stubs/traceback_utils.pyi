from _typeshed import Incomplete
from typing import NamedTuple

class CallSite(NamedTuple):
    function: Incomplete
    file: Incomplete
    linenum: Incomplete

def first_spark_call(): ...

class SCCallSiteSync:
    def __init__(self, sc) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, tb: types.TracebackType | None) -> None: ...
