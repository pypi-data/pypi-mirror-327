from typing_extensions import Literal
from pyspark.sql import DataFrame, functions as F


def fn(df1: DataFrame[Literal["source1", "source2"]]):
    df2 = df1.withColumn("c", F.col("source1"))
    df3 = df2.select(F.col("source1"))
    df4 = df3.withColumn("cd", F.col("source2"))  #  expect error
    df5 = df4.withColumn("cd", F.col("columnthatdoesnotexist"))  # expect error
    df6 = df5.alias("abcd")
    litcol = F.lit("ababdabadc").alias("litaliased")
    lit2 = F.lit("alit").alias("anotherlitaliased")
    expr = F.col("cd") == 1
    nonexistentcol = F.col("a").alias("aliased")
    existingconl = F.col("source1").alias("existent")
    cdcol = F.col("cd").alias("cd")
    df6 = df5.select(
        nonexistentcol,  # expect error
        existingconl,
        cdcol,
        F.col("source1"),
        expr.alias("expraliased"),
        litcol,
        lit2,
    )
    df7a = df6.select(
        *df6.columns,
    )

    df7 = df6.filter(expr)

    df8 = df7.select(F.col("cd"))
    expr2 = (F.col("cd") == F.lit("def")) & (F.col("cd") == "abc")
    df9 = df8.filter(expr2)
    df10 = df9.select(F.trim(F.col("cd")).alias("bbda"))
    df6.bcd  #  expect error
    df6.cd

    dfjoined = df10.join(df8, on=df10["bbda"] == df8["cd"], how="inner")
    resjoin = dfjoined.select(
        *df8.columns,
        df10["bbda"],
        F.trim(F.col("bbda")).alias('abcd'),
        F.col("nonexistent"), # expect error
    )
