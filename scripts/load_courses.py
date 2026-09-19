import pandas as pd

def main():
    courses = pd.read_csv("data/raw/courses_raw.csv")

    print(courses)
    print()
    print("Number of courses:", len(courses))
    print()
    print("Columns:")
    print(courses.columns.tolist())


if __name__ == "__main__":
    main()