import pandas as pd


INPUT_FILE = "data/raw/courses_raw.csv"
OUTPUT_FILE = "data/processed/courses_clean.csv"


def load_courses():
    return pd.read_csv(INPUT_FILE)


def normalize_text(df):
    text_columns = [
        "course_code",
        "title",
        "department",
        "description",
        "prerequisites_raw",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return df


def remove_duplicate_courses(df):
    before = len(df)

    df = df.drop_duplicates(subset=["course_code"], keep="first")

    removed = before - len(df)

    print(f"Removed {removed} duplicate courses")

    return df


def add_quality_flags(df):
    df["has_description"] = df["description"].str.len() > 0
    
    df["has_title"] = df["title"].str.len() > 0
    
    return df


NON_RECOMMENDABLE_KEYWORDS = [
    "independent study",
    "thesis",
    "dissertation",
    "co-op",
]


def add_recommendable_flag(df):
    def is_recommendable(title):
        title = title.lower()

        for keyword in NON_RECOMMENDABLE_KEYWORDS:
            if keyword in title:
                return False

        return True

    df["recommendable"] = df["title"].apply(is_recommendable)

    return df


def validate_courses(df):
    print("\nDataset validation")

    print("Total courses:", len(df))

    print("Missing descriptions:", (~df["has_description"]).sum())

    print("Non-recommendable courses:", (~df["recommendable"]).sum())

    print("\nCourses per department:")

    print(
        df.groupby("department")
        .size()
        .sort_values(ascending=False)
    )


def save_courses(df):
    df.to_csv(OUTPUT_FILE, index=False)

    print(
        f"\nSaved {len(df)} courses "
        f"to {OUTPUT_FILE}"
    )


def main():
    df = load_courses()

    print(f"Loaded {len(df)} raw courses")

    df = normalize_text(df)

    df = remove_duplicate_courses(df)

    df = add_quality_flags(df)

    df = add_recommendable_flag(df)

    validate_courses(df)

    save_courses(df)


if __name__ == "__main__":
    main()