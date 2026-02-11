from itertools import product, combinations
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


def get_sections_by_course(course_ids=None):
    db = SessionLocal()

    query = db.query(Schedule).filter(Schedule.type_course != "VT")
    if course_ids:
        query = query.filter(Schedule.course_id.in_(course_ids))

    schedules = query.all()

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

        # validar disponibilidad
        if not all(fits_availability(slot, availability) for slot in all_slots):
            continue

        # validar conflictos
        if has_conflict(all_slots):
            continue
        

        valid_combinations.append(all_slots)

    return valid_combinations


def time_overlap(a_start, a_end, b_start, b_end):
    return max(a_start, b_start) < min(a_end, b_end)


def schedules_conflict(section1, section2):
    for s1 in section1:
        for s2 in section2:
            if s1.day == s2.day:
                if time_overlap(s1.start, s1.end, s2.start, s2.end):
                    return True
    return False



def fits_availability(section, availability):
    for sch in section:
        day_availability = [a for a in availability if a.day == sch.day]

        valid = False
        for a in day_availability:
            if sch.start >= a.start and sch.end <= a.end:
                valid = True
                break

        if not valid:
            return False

    return True


def generate_valid_schedules(max_courses: int):
    db = SessionLocal()
    availability = db.query(Availability).all()
    db.close()

    grouped = get_sections_by_course()

    course_ids = list(grouped.keys())
    valid_combinations = []

    for course_combo in combinations(course_ids, max_courses):

        sections_lists = [grouped[cid] for cid in course_combo]

        # Convert dict of sections to list
        sections_product = []
        for section_dict in sections_lists:
            sections_product.append(list(section_dict.values()))

        # Producto cartesiano manual
        from itertools import product
        for combo in product(*sections_product):

            # Validar disponibilidad
            if not all(fits_availability(section, availability) for section in combo):
                continue

            # Validar conflictos
            conflict = False
            for i in range(len(combo)):
                for j in range(i + 1, len(combo)):
                    if schedules_conflict(combo[i], combo[j]):
                        conflict = True
                        break
                if conflict:
                    break

            if not conflict:
                valid_combinations.append(combo)

    return valid_combinations