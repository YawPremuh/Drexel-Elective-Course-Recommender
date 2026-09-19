import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timezone


DEPARTMENTS = {
    "CS": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/cs/",
    "ECE": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/ecec/",
    "ECEC": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/ecec/",
    "MATH": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/math/",
    "FIN": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/fin/",
    "ECON": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/econ/",
    "BUSN": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/busn/",
    "LAW": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/law/",
    "SWE": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/se/",
    "DSCI": "https://catalog.drexel.edu/coursedescriptions/quarter/undergrad/dsci/"

}

OUTPUT_FILE = "data/raw/courses_raw.csv"

def fetch_page(url):
    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "DrexelElectiveRecommender/1.0"
        },
    )

    response.raise_for_status()

    return response.text

def parse_course_title(title_text):

    pattern = (
        r"([A-Z]+)\s+"
        r"(\d+)\s+"
        r"(.+?)\s+"
        r"([\d.]+)\s+Credits"
    )

    match = re.match(pattern, title_text)

    if not match:
        return None

    department = match.group(1)
    course_number = int(match.group(2))
    title = match.group(3).strip()
    credits = float(match.group(4))

    course_code = f"{department}{course_number}"

    return {
        "course_code": course_code,
        "department": department,
        "course_number": course_number,
        "title": title,
        "credits": credits,
    }


def extract_prerequisites(block_text):
    if "Prerequisites:" not in block_text:
        return ""

    prerequisites = block_text.split(
        "Prerequisites:",
        1
    )[1].strip()

    return prerequisites


def parse_courses(html, source_url):
    soup = BeautifulSoup(html, "html.parser")

    courses = []

    course_blocks = soup.find_all("div", class_="courseblock")

    print(f"Found {len(course_blocks)} course blocks")

    for block in course_blocks:

        title_element = block.find(class_="courseblocktitle")

        description_element = block.find(class_="courseblockdesc")

        if not title_element:
            continue

        title_text = title_element.get_text(" ", strip=True)

        parsed_title = parse_course_title(title_text)

        if parsed_title is None:
            print(
                f"Could not parse course title: "
                f"{title_text}"
            )
            continue

        description = ""

        if description_element:
            description = (description_element.get_text(" ", strip=True))

        block_text = block.get_text(" ", strip=True)

        prerequisites_raw = (extract_prerequisites(block_text))

        course = {
            "course_code":
                parsed_title["course_code"],

            "title":
                parsed_title["title"],

            "department":
                parsed_title["department"],

            "course_number":
                parsed_title["course_number"],

            "description":
                description,

            "credits":
                parsed_title["credits"],

            "prerequisites_raw":
                prerequisites_raw,

            "catalog_year":
                "2026-2027",

            "calendar_system":
                "quarter",

            "source_url":
                source_url,

            "scraped_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        courses.append(course)

    return courses


def scrape_department(department, url):

    print(f"\nScraping {department}...")

    try:
        html = fetch_page(url)

        courses = parse_courses(html, url)

        print(
            f"{department}: "
            f"{len(courses)} courses parsed"
        )

        return courses

    except requests.RequestException as error:
        print(
            f"Failed to scrape "
            f"{department}: {error}"
        )

        return []

def scrape_department(department, url):

    print(f"\nScraping {department}...")

    try:
        html = fetch_page(url)

        courses = parse_courses(html, url)

        print(
            f"{department}: "
            f"{len(courses)} courses parsed"
        )

        return courses

    except requests.RequestException as error:
        print(
            f"Failed to scrape "
            f"{department}: {error}"
        )

        return []

def save_courses(courses):
    df = pd.DataFrame(courses)

    df.to_csv(OUTPUT_FILE, index=False)

    print(
        f"\nSaved {len(df)} courses "
        f"to {OUTPUT_FILE}"
    )



def parse_courses(html, source_url):
    soup = BeautifulSoup(html, "html.parser")

    courses = []

    course_blocks = soup.find_all("div", class_="courseblock")

    print(f"Found {len(course_blocks)} course blocks")

    for block in course_blocks:

        title_element = block.find(class_="courseblocktitle")

        description_element = block.find(class_="courseblockdesc")

        if not title_element:
            continue

        title_text = title_element.get_text(" ", strip=True)

        parsed_title = parse_course_title(title_text)

        if parsed_title is None:
            print(
                f"Could not parse course title: "
                f"{title_text}"
            )
            continue

        description = ""

        if description_element:
            description = (description_element.get_text(" ", strip=True))

        block_text = block.get_text(" ", strip=True)

        prerequisites_raw = (extract_prerequisites(block_text))

        course = {
            "course_code":
                parsed_title["course_code"],

            "title":
                parsed_title["title"],

            "department":
                parsed_title["department"],

            "course_number":
                parsed_title["course_number"],

            "description":
                description,

            "credits":
                parsed_title["credits"],

            "prerequisites_raw":
                prerequisites_raw,

            "catalog_year":
                "2026-2027",

            "calendar_system":
                "quarter",

            "source_url":
                source_url,

            "scraped_at":
                datetime.now(
                    timezone.utc
                ).isoformat(),
        }

        courses.append(course)

    return courses


def scrape_department(department, url):

    print(f"\nScraping {department}...")

    try:
        html = fetch_page(url)

        courses = parse_courses(html, url)

        print(
            f"{department}: "
            f"{len(courses)} courses parsed"
        )

        return courses

    except requests.RequestException as error:
        print(
            f"Failed to scrape "
            f"{department}: {error}"
        )

        return []

def save_courses(courses):
    df = pd.DataFrame(courses)
    df.to_csv("data/raw/courses_raw.csv", index=False)


def main():

    all_courses = []

    for department, url in DEPARTMENTS.items():

        courses = scrape_department(department, url)

        all_courses.extend(courses)

        time.sleep(1)

    save_courses(all_courses)

    print("\nScraping complete.")


if __name__ == "__main__":
    main()