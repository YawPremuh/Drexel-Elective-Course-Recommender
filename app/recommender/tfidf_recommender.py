import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


data_file = "data/processed/courses_clean.csv"

def load_courses():
    return pd.read_csv(data_file)

def filter_courses(courses):
    courses = courses.copy()

    if "recommendable" in courses.columns:
        courses = courses[courses["recommendable"] == True]

    if "has_description" in courses.columns:
        courses = courses[courses["has_description"] == True]

    return courses.reset_index(drop=True)

def build_course_text(courses):
    courses = courses.copy()

    courses["course_text"] = (
        courses["title"].fillna("")
        + " "
        + courses["description"].fillna("")
    )

    return courses

def create_tfidf_matrix(courses):
    vectorizer = TfidfVectorizer(stop_words="english")
    course_matrix = vectorizer.fit_transform(courses["course_text"])

    return vectorizer, course_matrix



def vectorize_student_interests(interests, vectorizer):
    return vectorizer.transform([interests])

def calculate_similarity(student_vector, course_matrix):
    similarities = cosine_similarity(student_vector, course_matrix)

    return similarities[0]

def rank_courses(courses, similarities, top_k=5):
    ranked = courses.copy()

    ranked["similarity_score"] = similarities

    ranked = ranked.sort_values("similarity_score", ascending=False)

    return ranked.head(top_k)

def recommend_courses(interests, top_k=5):
    courses = load_courses()

    courses = filter_courses(courses)

    courses = build_course_text(courses)

    vectorizer, course_matrix = (create_tfidf_matrix(courses))

    student_vector = vectorize_student_interests(interests, vectorizer)

    similarities = calculate_similarity(student_vector, course_matrix)

    recommendations = rank_courses(courses, similarities, top_k)

    return recommendations

def main():
    interests = input("Enter your interests: ")

    recommendations = recommend_courses(interests, top_k=5)

    print("\nRecommended Courses\n")

    for rank, (_, course) in enumerate(recommendations.iterrows(), start=1):
        print(
            f"{rank}. "
            f"{course['course_code']} - "
            f"{course['title']}"
        )

        print(
            f"   Department: "
            f"{course['department']}"
        )

        print(
            f"   Score: "
            f"{course['similarity_score']:.4f}"
        )

        print()


if __name__ == "__main__":
    main()