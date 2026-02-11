from sqlalchemy import Column, String, Integer, ForeignKey, Time, Boolean
from sqlalchemy.orm import relationship
from .db import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True)
    code = Column(String)
    name = Column(String)
    hours = Column(Integer)
    credits = Column(Integer)
    type = Column(String)
    cycle = Column(Integer)

    schedules = relationship("Schedule", back_populates="course")


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("courses.id"))
    section = Column(Integer)
    day = Column(Integer)  # 1 = lunes
    start = Column(Time)
    end = Column(Time)
    teacher = Column(String)
    type_course = Column(String)

    course = relationship("Course", back_populates="schedules")



class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    day = Column(Integer)  # 1-7
    start = Column(Time)
    end = Column(Time)
