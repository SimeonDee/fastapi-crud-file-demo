from typing import Optional
from pydantic import BaseModel


class Student(BaseModel):
    username: Optional[str] = ""
    password: Optional[str] = None
    profile_pix: Optional[str] = ""
    matric: str
    name: str
    age: int


class StudentGet(BaseModel):
    username: Optional[str] = ""
    profile_pix: Optional[str] = ""
    matric: str
    name: str
    age: int


class StudentCreate(BaseModel):
    username: Optional[str] = ""
    password: Optional[str] = ""
    matric: str
    name: str
    age: int


class StudentUpdate(BaseModel):
    username: Optional[str] = ""
    password: Optional[str] = ""
    profile_pix: Optional[str] = ""
    matric: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
