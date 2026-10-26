import pandas as pd

from data_processor import (
    generate_data_quality_report,
    clean_dataset,
)



def main():
    sample_data = pd.DataFrame({
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
        ],
        "Employees": [
            25,
            10,
            25,
            15,
        ],
        "Performance": [
            85,
            78,
            85,
            None,
        ],
    })

    print("ORIGINAL DATASET")
    print(sample_data)

    print("\nDATA QUALITY REPORT")
    report = generate_data_quality_report(sample_data)

    for key, value in report.items():
        print(f"{key}: {value}")

    print("\nCLEANING DATASET")
    cleaned_df, summary = clean_dataset(sample_data)

    print(cleaned_df)

    print("\nCLEANING SUMMARY")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()