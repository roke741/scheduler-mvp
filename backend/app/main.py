from fastapi import FastAPI, Query
from .db import engine
from .models import Base
from app.services.scheduler import generate_combinations, generate_valid_schedules
from app.schemas import AvailabilityCreate
from app.models import Availability
from app.db import SessionLocal
from fastapi.responses import FileResponse
from app.services.exporter import export_schedule_to_excel


app = FastAPI(title="Scheduler MVP")


@app.get("/combinations")
def combinations(
    courses: str,
    user_id: str
):
    course_ids = courses.split(",")

    combos = generate_combinations(course_ids, user_id)

    result = []

    for combo in combos:
        result.append([
            {
                "course_id": s.course_id,
                "section": s.section,
                "day": s.day,
                "start": s.start.strftime("%H:%M"),
                "end": s.end.strftime("%H:%M"),
                "teacher": s.teacher
            }
            for s in combo
        ])

    return {
        "total": len(result),
        "combinations": result
    }


@app.post("/availability")
def create_availability(data: AvailabilityCreate):
    db = SessionLocal()

    availability = Availability(
        user_id=data.user_id,
        day=data.day,
        start=data.start,
        end=data.end
    )

    db.add(availability)
    db.commit()
    db.refresh(availability)
    db.close()

    return {
        "message": "Availability created",
        "id": availability.id
    }

@app.post("/recommend-schedule")
def recommend_schedule(max_courses: int = 4):
    schedules = generate_valid_schedules(max_courses)

    result = []

    for combo in schedules:
        formatted = []
        for section in combo:
            formatted.append({
                "course_id": section[0].course_id,
                "section": section[0].section,
                "day_blocks": [
                    {
                        "day": s.day,
                        "start": s.start,
                        "end": s.end
                    }
                    for s in section
                ]
            })
        result.append(formatted)

    return {
        "total_options": len(result),
        "options": result[:10]  # limitar a 10 para no explotar
    }

@app.post("/export-schedule")
def export_schedule(max_courses: int = 4):

    schedules = generate_valid_schedules(max_courses)

    if not schedules:
        return {"message": "No hay combinaciones válidas"}

    # Tomamos la primera opción como ejemplo
    combo = schedules[0]

    formatted = []
    for section in combo:
        formatted.append({
            "course_id": section[0].course_id,
            "section": section[0].section,
            "day_blocks": [
                {
                    "day": s.day,
                    "start": s.start,
                    "end": s.end
                }
                for s in section
            ]
        })

    file_path = "recommended_schedule.xlsx"
    export_schedule_to_excel(formatted, file_path)

    return FileResponse(
        path=file_path,
        filename="recommended_schedule.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
