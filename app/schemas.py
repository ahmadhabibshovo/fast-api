from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime

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

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class SocialLoginRequest(BaseModel):
    token: str
