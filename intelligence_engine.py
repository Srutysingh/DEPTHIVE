import pandas as pd


def analyze_department_performance(df):
    """
    Analyze department-wise performance using available KPI data.
    """

    if df is None or df.empty:
        return {
            "success": False,
            "message": "No data available for analysis."
        }

    # Check whether Department column exists
    if "Department" not in df.columns:
        return {
            "success": False,
            "message": "Dataset must contain a 'Department' column."
        }

    # Identify numeric KPI columns
    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    if not numeric_columns:
        return {
            "success": False,
            "message": "No numeric KPI columns found."
        }

    # Calculate department-wise KPI averages
    department_performance = (
        df.groupby("Department")[numeric_columns]
        .mean()
        .round(2)
    )

    # Calculate an overall score from numeric KPIs
    department_performance["Performance Score"] = (
        department_performance[numeric_columns]
        .mean(axis=1)
        .round(2)
    )

    # Rank departments
    department_performance["Rank"] = (
        department_performance["Performance Score"]
        .rank(method="dense", ascending=False)
        .astype(int)
    )

    # Classify performance using relative scores
    average_score = department_performance[
        "Performance Score"
    ].mean()

    def classify_performance(score):
        if score >= average_score * 1.10:
            return "High"
        elif score >= average_score * 0.90:
            return "Moderate"
        else:
            return "Low"

    department_performance["Performance Level"] = (
        department_performance["Performance Score"]
        .apply(classify_performance)
    )

    department_performance = department_performance.sort_values(
        by="Performance Score",
        ascending=False
    )

    return {
        "success": True,
        "message": "Department analysis completed successfully.",
        "department_performance": department_performance,
        "top_department": department_performance.index[0],
        "total_departments": len(department_performance)
    }