from fastapi import FastAPI, Query
from .db import engine
from .models import Base
from app.services.scheduler import generate_combinations
from app.schemas import AvailabilityCreate
from app.models import Availability
from app.db import SessionLocal

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


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def health():
    return {"status": "ok"}
