import pandas as pd

required_columns = [
    "course_code",
    "title",
    "department",
    "course_number",
    "description",
    "credits",
    "prerequisites_raw",
    "prerequisite_courses",
    "catalog_year",
    "calendar_system",
]


def main():
    courses = pd.read_csv("data/raw/courses_raw.csv")

    print("Checking dataset...\n")

    # Check columns
    missing_columns = [
        column
        for column in required_columns
        if column not in courses.columns
    ]

    if missing_columns:
        print("Missing columns:", missing_columns)
    else:
        print("All required columns exist.")

    duplicates = courses[courses["course_code"].duplicated()]

    if len(duplicates) > 0:
        print("Duplicate courses found:")
        print(duplicates)
    else:
        print("No duplicate course codes.")

    important_columns = [
        "course_code",
        "title",
        "description",
        "department",
    ]

    print("\nMissing values:")
    print(courses[important_columns].isnull().sum())

    print("\nTotal courses:", len(courses))


if __name__ == "__main__":
    main()