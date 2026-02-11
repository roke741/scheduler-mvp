import os
import requests

GRAPHQL_URL = "https://api-portal.utpxpedition.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    #"Authorization": f"Bearer {os.getenv('GRAPHQL_TOKEN')}",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI4MWJhODBaRjZTYkFrMWNjY2dGMkoyVGFybjFJLV90U0N4NjhPWGI5N3QwIn0.eyJleHAiOjE3NzA4NTk5MjIsImlhdCI6MTc3MDc3MzUyMiwiYXV0aF90aW1lIjoxNzcwNzczNTIxLCJqdGkiOiI5ZmZjNTFiNy1kODY5LTQ4NTMtYTc0My03ZDExNzlmZGI5YjIiLCJpc3MiOiJodHRwczovL3Nzby51dHAuZWR1LnBlL2F1dGgvcmVhbG1zL1hwZWRpdGlvbiIsImF1ZCI6WyJwYW8td2ViIiwiYWNjb3VudCJdLCJzdWIiOiI4OGViY2IxNy05NGU2LTQ1MDAtYWRiYS1iMWVjOTNkOTJiNTUiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJ1dHBtYXMtd2ViIiwibm9uY2UiOiIyMDRiYTY1Yy0wYTQwLTQ0NDEtODhiZS1lNjRhY2Q0YWRlNmMiLCJzZXNzaW9uX3N0YXRlIjoiYTZlNjRlM2MtNmI4OS00ZTdmLWE3NzgtZmVmYTZjZjY0MDFjIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vcG9ydGFsLnV0cC5lZHUucGUiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImRlZmF1bHQtcm9sZXMteHBlZGl0aW9uIiwic3R1ZGVudCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJwYW8td2ViIjp7InJvbGVzIjpbInN0dWRlbnQiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgcm9sZXMtcmVhbG0teHBlZGl0aW9uIiwic2lkIjoiYTZlNjRlM2MtNmI4OS00ZTdmLWE3NzgtZmVmYTZjZjY0MDFjIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLXhwZWRpdGlvbiIsInN0dWRlbnQiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl0sIm5hbWUiOiJKT1JESUUgSkVGRkVSU09OIFJPUVVFIFlBVUxJIiwicHJlZmVycmVkX3VzZXJuYW1lIjoidTI0MjU0NzA3IiwiZ2l2ZW5fbmFtZSI6IkpPUkRJRSBKRUZGRVJTT04iLCJmYW1pbHlfbmFtZSI6IlJPUVVFIFlBVUxJIiwiZW1haWwiOiJ1MjQyNTQ3MDdAdXRwLmVkdS5wZSJ9.HZ9mHhwEoRpGXwHDy6NBC9X6AT6wRXQjmA606d5u2518U_KIcXfeu3kshkEz5L4YhJ8aIcUwwd2SaxO4CUdo5PRqq2X4sxjQN165z0eb-D28lpDK-jZL6QRHwa18jfNmtRTVyAGKSDtzWLZBcAIVlesd0IajSJd5udshbq1C9k9jc93G6DejKpur57gimPIzdvTsvGhWW60Ook-rrirn3PR7Sr2saCK0QzUyND1UD-lk133k2fB3CBIabXT75_65vlhMmK7ipMze2V9l3xoLdihHcViu-V8dG7LArvQSe6paCp1UYZb3H3W6hXqmL4TFpPWh2lg6yl2pX8HqwpQBJA",
    "User-Id": "u24254707",
    "User-Role": "student"
}

BASE_VARS = {
    "campus": "AREQU",
    "career": "PREG",
    "plan": "SIST2652",
    "prog": "PST50",
    "period": "2262",
}

GET_COURSES_QUERY = """
query getEnrollmentCourses(
  $period: String!,
  $prog: String!,
  $plan: String!,
  $career: String!,
  $campus: String!
) {
  coursesSchedules {
    getCourses(
      period: $period
      prog: $prog
      plan: $plan
      career: $career
      campus: $campus
    ) {
      id
      code
      name
      hours
      credits
      type
      cicle
    }
  }
}
"""


def fetch_courses():
    payload = {
        "operationName": "getEnrollmentCourses",
        "query": GET_COURSES_QUERY,
        "variables": BASE_VARS,
    }

    print("➡️ Fetching courses...")
    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)

    print("⬅️ Status:", r.status_code)
    print("⬅️ Response:", r.text[:500])  # solo primeros chars

    r.raise_for_status()

    data = r.json()
    return data["data"]["coursesSchedules"]["getCourses"]




GET_SCHEDULES_QUERY = """
query getRegistrationTimes(
  $courseId: String!,
  $period: String!,
  $prog: String!,
  $plan: String!,
  $career: String!,
  $campus: String!
) {
  coursesSchedules {
    getSchedules(
      courseId: $courseId
      period: $period
      prog: $prog
      plan: $plan
      career: $career
      campus: $campus
    ) {
      courseId
      section
      schedules {
        day
        start
        end
      }
      teachers
      typeCourse
    }
  }
}
"""

def fetch_schedules(course_id: str):
    variables = BASE_VARS | {"courseId": course_id}

    payload = {
        "operationName": "getRegistrationTimes",
        "query": GET_SCHEDULES_QUERY,
        "variables": variables,
    }

    print(f"➡️ Fetching schedules for course {course_id}")
    r = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)

    print("⬅️ Status:", r.status_code)
    print("⬅️ Response:", r.text[:500])

    r.raise_for_status()

    data = r.json()
    return data["data"]["coursesSchedules"]["getSchedules"]

