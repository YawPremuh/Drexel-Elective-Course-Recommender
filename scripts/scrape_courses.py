import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/cs/"


def fetch_page(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    return response.text


def parse_courses(html):
    soup = BeautifulSoup(html, "html.parser")

    courses = []

    course_blocks = soup.find_all("div",class_="courseblock")

    for block in course_blocks:

        title_element = block.find(class_="courseblocktitle")

        description_element = block.find(class_="courseblockdesc")

        if not title_element:
            continue

        title_text = title_element.get_text(" ", strip=True)

        description = ""

        if description_element:
            description = description_element.get_text(" ", strip=True)

        pattern = (
            r"([A-Z]+)\s+"
            r"(\d+)\s+"
            r"(.+?)\s+"
            r"([\d.]+)\s+Credits"
        )

        match = re.match(pattern, title_text)

        if not match:
            continue

        department = match.group(1)

        course_number = int(match.group(2))

        title = match.group(3)

        credits = float(match.group(4))

        course_code = (f"{department}{course_number}")

        block_text = block.get_text(" ", strip=True)

        prerequisites_raw = ""

        if "Prerequisites:" in block_text:
            prerequisites_raw = (
                block_text
                .split("Prerequisites:", 1)[1]
                .strip()
            )

        course = {
            "course_code": course_code,
            "title": title,
            "department": department,
            "course_number": course_number,
            "description": description,
            "credits": credits,
            "prerequisites_raw": prerequisites_raw,
            "catalog_year": "2026-2027",
            "calendar_system": "quarter"
        }

        courses.append(course)

    return courses


def save_courses(courses):
    df = pd.DataFrame(courses)
    df.to_csv("data/raw/courses_raw.csv", index=False)


def main():
    html = fetch_page(URL)
    courses = parse_courses(html)
    print(f"Found {len(courses)} courses")
    save_courses(courses)


if __name__ == "__main__":
    main()