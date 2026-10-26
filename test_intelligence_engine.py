import pandas as pd

from intelligence_engine import analyze_department_performance


def test_department_analysis():
    df = pd.DataFrame({
        "Department": [
            "Engineering",
            "Engineering",
            "Marketing",
            "Marketing",
            "Sales",
            "Sales"
        ],
        "Productivity": [90, 85, 70, 75, 80, 82],
        "Efficiency": [88, 92, 72, 74, 85, 83]
    })

    result = analyze_department_performance(df)

    assert result["success"] is True
    assert result["total_departments"] == 3
    assert result["top_department"] == "Engineering"

    print("\nDepartment Performance:")
    print(result["department_performance"])

    print("\nTop Department:", result["top_department"])
    print("Total Departments:", result["total_departments"])
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_department_analysis()