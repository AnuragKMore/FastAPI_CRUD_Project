from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: int
    joiningdate: str
    skills: List[str]
