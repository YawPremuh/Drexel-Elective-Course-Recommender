# Drexel Elective Course Recommender

A personalized course recommendation system designed to help Drexel University students discover electives based on their interests, academic background, career goals, and course preferences.

## Problem

Choosing electives at Drexel can be time-consuming and frustrating.

Students often need to search through multiple sources such as:

- Drexel course catalogs
- Reddit discussions
- Professor reviews
- Course prerequisites
- Student recommendations

This project aims to reduce that friction by providing students with a ranked list of relevant electives in one place.

## Goal

The long-term goal is to build a hybrid recommendation system that considers:

- Student interests
- Career goals
- Completed courses
- Course prerequisites
- Course content
- Professor ratings
- Difficulty and workload
- Student feedback and interactions

The system will eventually return personalized course recommendations with explanations for why each course was recommended.

## System Architecture
```text
                 Student Profile
                       |
                       v
               Profile Builder
                       |
                       v
              Candidate Filtering
                       |
           -------------------------
           |           |           |
           v           v           v
      Prerequisites  Completed    Major
         Filter      Courses      Rules
           |           |           |
           -------------------------
                       |
                       v
              Candidate Retrieval
                       |
                       v
                  Hybrid Ranker
              -------------------
              |        |        |
              v        v        v
          Semantic   Career   Community
           Score     Score     Score
              |        |        |
              -------------------
                       |
                       v
                Top-K Courses
                       |
                       v
             Explanation Engine
                       |
                       v
                    FastAPI
                       |
                       v
                    Web App
```

---

## Current Project Status

### Phase 1 — Problem Definition
Completed

Defined:

- Target users
- Recommendation inputs
- Course features
- Recommendation outputs
- Hard eligibility constraints
- Ranking signals
- MVP requirements

### Phase 2 — Course Data Collection
Completed

Built a web scraper for the Drexel University course catalog.

Current supported departments include:

- CS
- ECEC
- SE
- DSCI
- MATH
- FIN
- ECON
- BUSN
- LAW

Current raw dataset:

```text
246 courses
```

### Phase 4
## TF-IDF Baseline Results

The current baseline represents course titles and descriptions using TF-IDF and ranks courses using cosine similarity.

The processed dataset contains:

- 224 cleaned courses
- 223 courses with usable descriptions
- 2,127 TF-IDF features

### Example: Machine Learning

Input:

```text
machine learning artificial intelligence data science
```