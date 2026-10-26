import pandas as pd
from io import BytesIO


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


def load_dataset(file):
    """Load a CSV or Excel file into a pandas DataFrame."""

    filename = file.name.lower()

    if not any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
        raise ValueError("Unsupported file format. Upload CSV or XLSX.")

    try:
        file_bytes = file.getvalue()

        if not file_bytes:
            raise ValueError("The uploaded file is empty.")

        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(file_bytes))
        else:
            df = pd.read_excel(BytesIO(file_bytes), engine="openpyxl")

    except (pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        raise ValueError(f"Could not read the CSV file: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Could not read the uploaded file: {exc}") from exc

    if df.empty:
        raise ValueError("The dataset contains no data rows.")

    if len(df.columns) == 0:
        raise ValueError("The dataset contains no columns.")

    return df


def generate_data_quality_report(df):
    """Generate a data-quality report for a DataFrame."""

    if df.empty:
        raise ValueError("Cannot analyze an empty dataset.")

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "columns_with_missing_values": int(
            df.isna().any(axis=0).sum()
        ),
        "column_names": df.columns.tolist(),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values_by_column": {
            column: int(count)
            for column, count in df.isna().sum().items()
        },
    }


def clean_dataset(df):
    """Return a cleaned copy without duplicate rows."""

    if df.empty:
        raise ValueError("Cannot clean an empty dataset.")

    cleaned_df = df.copy()
    original_rows = len(cleaned_df)

    cleaned_df = cleaned_df.drop_duplicates().reset_index(drop=True)

    summary = {
        "original_rows": original_rows,
        "cleaned_rows": len(cleaned_df),
        "duplicates_removed": original_rows - len(cleaned_df),
        "missing_cells_remaining": int(
            cleaned_df.isna().sum().sum()
        ),
    }

    return cleaned_df, summary