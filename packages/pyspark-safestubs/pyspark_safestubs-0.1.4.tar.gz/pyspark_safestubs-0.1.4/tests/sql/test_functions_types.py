from typing import TYPE_CHECKING, Literal, TypeVar
from typing_extensions import LiteralString

from pyspark.sql import functions as F, DataFrame
from pyspark.sql.column import Column
from pyspark.sql.window import WindowSpec

if TYPE_CHECKING:
    try:
        from typing import assert_type  # type: ignore
    except ImportError:
        from typing_extensions import assert_type
    from pyspark.sql.session import SparkSession

T = TypeVar("T", bound=LiteralString)


def some_processing(
    df: DataFrame[T],
    sbti_df: DataFrame[Literal["df2_id", "df2_somecol2", "test2"]],
    active_year_col: T,
    bvd_col_name: T,
):
    selected = df.join(
        sbti_df,
        on=(
            F.col(active_year_col)
            == sbti_df["df2_id"] & (F.col(bvd_col_name) == sbti_df["df2_id"])
        ),
        how="left",
    ).select(
        *df.columns,
        F.col("df2_id").alias("df2_aliased"),
        F.col("df2_somecol2").alias("df2_somecol2_aliased"),
        F.lit(1).alias("lit_col"),
    )
    return selected


def test_some_processing(
    df1: DataFrame[Literal["df1_id", "df1_somecol1", "df1_somecol2", "df1_somecol3"]],
    df2: DataFrame[Literal["df2_id", "df2_somecol2", "test2"]],
) -> None:
    result = some_processing(
        df=df1,
        sbti_df=df2,
        active_year_col="df1_somecol1",
        bvd_col_name="df1_somecol2",
    )
    assert_type(
        result,
        DataFrame[
            Literal[
                "df1_id",
                "df1_somecol1",
                "df1_somecol2",
                "df1_somecol3",
                "df2_aliased",
                "df2_somecol2_aliased",
                "lit_col",
            ]
        ],
    )


def test_column_type_propagation() -> None:
    # Test that column name type is preserved
    col1 = F.col("test_col")
    assert_type(col1, Column[Literal["test_col"], Literal["test_col"]])

    # Test literal
    lit_col = F.lit(1)
    assert_type(lit_col, Column[Literal["lit"], Literal["expr"]])

    # Test that column operations preserve input type
    col2 = F.col("name")
    upper_col = F.upper(col2)
    assert_type(upper_col, Column[Literal["name"], Literal["expr"]])

    # Test multiple column operations
    col3 = F.col("age")
    sum_col = F.sum(col3)
    assert_type(sum_col, Column[Literal["age"], Literal["expr"]])

    # Test when condition
    when_col = F.when(F.col("flag") == F.lit(True), 1).otherwise(0)
    assert_type(when_col, Column[Literal["flag", "lit"], Literal["expr"]])


def test_string_operations() -> None:
    # Test string functions
    str_col = F.col("text")
    concat = F.concat(str_col, F.lit(" suffix"))
    assert_type(concat, Column[Literal["text", "lit"], Literal["expr"]])

    # Test regexp
    regex = F.regexp_replace(str_col, "pattern", "replacement")
    assert_type(regex, Column[Literal["text"], Literal["expr"]])


def test_math_operations() -> None:
    # Test math functions
    num_col = F.col("number")
    abs_col = F.abs(num_col)
    assert_type(abs_col, Column[Literal["number"], Literal["expr"]])

    # Test round
    round_col = F.round(num_col, 2)
    assert_type(round_col, Column[Literal["number"], Literal["expr"]])


def test_aggregation_operations() -> None:
    # Test aggregation functions
    val_col = F.col("value")
    avg_col = F.avg(val_col)
    assert_type(avg_col, Column[Literal["value"], Literal["expr"]])

    # Test count
    count_col = F.count(val_col)
    assert_type(count_col, Column[Literal["lit"], Literal["expr"]])


def test_complex_when_regexp() -> None:
    # Test complex when conditions with regexp and date conversions
    date_col = F.col("date_string")

    # Complex when chain with regexp patterns and date conversions
    parsed_date = (
        F.when(
            F.regexp_like(date_col, F.lit(r"^\d{4}-\d{2}-\d{2}$")),
            F.to_date(date_col, "yyyy-MM-dd"),
        )
        .when(
            F.regexp_like(date_col, F.lit(r"^\d{2}/\d{2}/\d{4}$")),
            F.to_date(date_col, "MM/dd/yyyy"),
        )
        .otherwise(F.lit(None))
    )

    assert_type(parsed_date, Column[Literal["date_string", "lit"], Literal["expr"]])

    # Test with multiple regexp conditions combined
    complex_date = F.when(
        F.regexp_like(date_col, F.lit(r"^\d{4}"))
        & F.regexp_like(date_col, F.lit(r"\d{2}$")),
        F.to_date(date_col, "yyyy-MM-dd"),
    ).otherwise(F.current_date())

    assert_type(complex_date, Column[Literal["date_string", "lit"], Literal["expr"]])


def test_boolean_operations() -> None:
    # Test negation operator
    bool_col = F.col("flag")
    negated = ~bool_col
    assert_type(negated, Column[Literal["flag"], Literal["flag"]])

    # Test combined boolean operations
    combined = ~(bool_col & F.col("other_flag"))
    assert_type(combined, Column[Literal["flag", "other_flag"], Literal["expr"]])


def test_regexp_operations() -> None:
    # Test regexp_like
    text_col = F.col("text")
    pattern = "^[A-Z].*"

    # Basic regexp_like
    matches = F.regexp_like(text_col, pattern)
    assert_type(matches, Column[Literal["text"], Literal["expr"]])

    # regexp_like with case sensitivity flag

    # Combining regexp_like with other operations
    combined = ~F.regexp_like(text_col, pattern)
    assert_type(combined, Column[Literal["text"], Literal["expr"]])


if TYPE_CHECKING:
    from pyspark.sql.dataframe import DataFrame
    from pyspark.sql.session import SparkSession

    def test_dataframe_pipeline_types(spark: SparkSession) -> None:
        data = [("John", 30, 5000.0, "IT")]
        df = spark.createDataFrame(data, ("name", "age", "salary", "dept"))
        assert_type(
            df,
            DataFrame[Literal["name", "age", "salary", "dept"]],
        )

        # Select and rename columns
        df2 = df.select(
            F.col("name"),
            F.col("age"),
            F.col("salary").alias("annual_salary"),
            F.lit("2024").alias("year"),
        )
        assert_type(df2, DataFrame[Literal["name", "age", "annual_salary", "year"]])

        # Add calculated columns
        df3 = (
            df2.withColumn("salary_monthly", F.col("annual_salary") / 12)
            .withColumn("age_next_year", F.col("age") + 1)
            .withColumn("name_upper", F.upper(F.col("name")))
        )
        assert_type(
            df3,
            DataFrame[
                Literal[
                    "name",
                    "age",
                    "annual_salary",
                    "year",
                    "salary_monthly",
                    "age_next_year",
                    "name_upper",
                ]
            ],
        )

        # Filter data

        df4 = df3.filter(
            (F.col("salary_monthly") > 400) & F.col("name_upper").startswith("A")
        )

        assert_type(
            df4,
            DataFrame[
                Literal[
                    "age",
                    "age_next_year",
                    "name_upper",
                    "salary_monthly",
                    "annual_salary",
                    "year",
                    "name",
                ]
            ],
        )

        # Aggregate operations
        summary = df4.groupBy("year").agg(
            F.count("*").alias("employee_count"),
            F.avg(F.col("salary_monthly")).alias("avg_salary"),
            F.collect_list(F.col("name_upper")).alias("employees"),
        )
        assert_type(
            summary,
            DataFrame[Literal["year", "employee_count", "avg_salary", "employees"]],
        )

        # Window functions
        from pyspark.sql import Window
        partitionedWin = Window.partitionBy("year")
        assert_type(partitionedWin, WindowSpec[Literal["year"]])
        window_spec = partitionedWin.orderBy(F.col("salary_monthly").desc())
        df5 = df4.withColumn("salary_rank", F.rank().over(window_spec)).withColumn(
            "running_total", F.sum("salary_monthly").over(window_spec)
        )
        assert_type(
            df5,
            DataFrame[
                Literal[
                    "name",
                    "age",
                    "annual_salary",
                    "year",
                    "salary_monthly",
                    "age_next_year",
                    "name_upper",
                    "salary_rank",
                    "running_total",
                ]
            ],
        )
