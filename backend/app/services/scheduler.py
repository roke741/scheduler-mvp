from itertools import product
from collections import defaultdict
from app.db import SessionLocal
from app.models import Schedule, Availability


def overlaps(a, b):
    return a.start < b.end and b.start < a.end


def has_conflict(slots):
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            if slots[i].day == slots[j].day:
                if overlaps(slots[i], slots[j]):
                    return True
    return False


def get_sections_by_course(course_ids):
    db = SessionLocal()

    schedules = (
        db.query(Schedule)
        .filter(Schedule.course_id.in_(course_ids), Schedule.type_course != "VT")
        .all()
    )

    db.close()

    grouped = defaultdict(lambda: defaultdict(list))

    for s in schedules:
        grouped[s.course_id][s.section].append(s)

    return grouped


def get_user_availability(user_id):
    db = SessionLocal()
    rows = db.query(Availability).filter(Availability.user_id == user_id).all()
    db.close()

    availability = {}

    for r in rows:
        availability.setdefault(r.day, []).append(r)

    return availability


def fits_availability(slot, availability):
    if slot.day not in availability:
        return False

    for window in availability[slot.day]:
        if slot.start >= window.start and slot.end <= window.end:
            return True

    return False


def generate_combinations(course_ids, user_id):
    grouped = get_sections_by_course(course_ids)
    availability = get_user_availability(user_id)

    section_lists = []

    for course_id in course_ids:
        sections = list(grouped[course_id].values())
        section_lists.append(sections)

    valid_combinations = []

    for combo in product(*section_lists):
        all_slots = [slot for section in combo for slot in section]

        # 1 validar disponibilidad
        if not all(fits_availability(slot, availability) for slot in all_slots):
            continue

        # 2 validar conflictos
        if has_conflict(all_slots):
            continue

        valid_combinations.append(all_slots)

    return valid_combinations
