from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional

class CourseBase(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[float] = None
    website: Optional[HttpUrl] = None

class Course(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
