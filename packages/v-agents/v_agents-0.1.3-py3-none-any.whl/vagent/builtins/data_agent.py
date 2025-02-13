from typing import TYPE_CHECKING
from vagent.core import llm_program, VContext

if TYPE_CHECKING:
    from pandas import DataFrame


def execute_sql_on_dataframe(df: "DataFrame", sql: str) -> "DataFrame":
    """Execute SQL on a pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to execute the SQL on.
        sql (str): The SQL to execute.
    Returns:
        pd.DataFrame: The resulting DataFrame.
    """
    try:
        import duckdb
    except ImportError:
        raise ImportError("Please install the duckdb package to use this tool.")
    return duckdb.query(f"{sql}").to_df()


@llm_program(
    model="meta-llama/Llama-3.3-70B-Instruct", temperature=0.3, max_tokens=1024
)
def summarize(ctx: VContext, prompt: str) -> str:
    """You are a helpful assistant in summarizing context and produce human-understandable summaries."""
    return f"Summarize the following: {prompt}."
