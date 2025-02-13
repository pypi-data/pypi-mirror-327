# Safer Stubs for PySpark

This is a project to create safer stubs for PySpark. The goal is to make it easier to use PySpark in a safer way, without having to worry about the underlying implementation.
It implements only subset of working PySpark APIs with goal to have a minimal set of functions that can be used in a safer way.

## How to use

To use the stubs, you need to install the package:

```bash
pip install pyspark-safestubs
```

Then, you can use the stubs in your code:

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def some_transform(df: DataFrame['col1', 'col2']):
    df = df.withColumn('col5', F.col('col1').cast('int'))
    # df has type DataFrame['col1', 'col2', 'col5']
    return df

```
