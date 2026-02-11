from datetime import time
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Course, Schedule
from .graphql import fetch_courses, fetch_schedules

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)



DAY_MAP = {
    "Lunes": 1,
    "Martes": 2,
    "Miércoles": 3,
    "Jueves": 4,
    "Viernes": 5,
    "Sábado": 6,
}

def parse_time(t: str):
    h, m = t.split(":")
    return time(int(h), int(m))


def run():
    logger.info("🚀 Starting data ingestion")

    db: Session = SessionLocal()

    courses = fetch_courses()
    logger.info(f"📚 Courses received: {len(courses)}")

    for c in courses:
        logger.info(f"➕ Inserting course {c['id']} - {c['name']}")

        course = Course(
            id=c["id"],
            code=c["code"],
            name=c["name"],
            hours=c["hours"],
            credits=c["credits"],
            type=c["type"],
            cycle=c["cicle"],
        )

        db.merge(course)
        db.commit()
        logger.info("✅ Course committed")

        schedules = fetch_schedules(c["id"])
        logger.info(f"🕒 Schedules received: {len(schedules)}")

        for s in schedules:
            for slot in s["schedules"]:
                logger.info(
                    f"   ➕ Slot day={slot['day']} {slot['start']}-{slot['end']}"
                )

                sch = Schedule(
                    course_id=c["id"],
                    section=s["section"],
                    day=DAY_MAP.get(slot["day"]),
                    start=parse_time(slot["start"]),
                    end=parse_time(slot["end"]),
                    teacher=", ".join(s["teachers"]),
                    type_course=s["typeCourse"],
                )
                db.add(sch)

        db.commit()
        logger.info("✅ Schedules committed")

    db.close()
    logger.info("🎉 Ingestion finished")


if __name__ == "__main__":
    run()
