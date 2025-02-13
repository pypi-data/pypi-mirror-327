from pyspark.pandas.data_type_ops.base import DataTypeOps as DataTypeOps

class UDTOps(DataTypeOps):
    @property
    def pretty_name(self) -> str: ...
