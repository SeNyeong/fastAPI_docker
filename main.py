from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist
from typing import List

# 학점 변환표 (A0, B0 등 포함)
GRADE_MAP = {
    "A+": 4.5, "A0": 4.0,
    "B+": 3.5, "B0": 3.0,
    "C+": 2.5, "C0": 2.0,
    "D+": 1.5, "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: conlist(Course, min_length=1)

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

app = FastAPI()

@app.post("/score")
def calculate_score(data: StudentRequest):
    total_score = 0.0
    total_credits = 0
    for course in data.courses:
        if course.grade not in GRADE_MAP:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        total_score += GRADE_MAP[course.grade] * course.credits
        total_credits += course.credits
    if total_credits == 0:
        gpa = 0.0
    else:
        gpa = round(total_score / total_credits + 1e-8, 3)  # 소수점 셋째자리 반올림
    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }
