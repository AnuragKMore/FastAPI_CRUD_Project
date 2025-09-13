from fastapi import APIRouter, HTTPException, Body
from models import Employee
from database import employees
from typing import Optional

router = APIRouter()

@router.post("/employees")
def create_employee(emp: Employee):
    if employees.find_one({"employee_id": emp.employee_id}):
        raise HTTPException(400, "employee_id must be unique")
    employees.insert_one(emp.dict())
    return {"success": True}

@router.get("/employees/avg-salary")
def avg_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"_id": 0, "department": "$_id", "avg_salary": 1}}
    ]

    try:
        result = list(employees.aggregate(pipeline))
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employees/search")
def search_employees(skill: str):
    emps = list(employees.find({"skills": skill}, {"_id": 0}))
    if not emps:
        raise HTTPException(status_code=404, detail="No employees found with that skill")
    return emps

@router.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    emp = employees.find_one({"employee_id": employee_id}, {"_id": 0})
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp

@router.put("/employees/{employee_id}")
def update_employee(employee_id: str, update: dict = Body(...)):
    result = employees.update_one({"employee_id": employee_id}, {"$set": update})
    if result.matched_count == 0:
        raise HTTPException(404, "Employee not found")
    return {"success": True}

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    result = employees.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Employee not found")
    return {"success": True}

@router.get("/employees")
def list_by_department(department: Optional[str] = None):
    query = {"department": department} if department else {}
    emps = list(employees.find(query, {"_id": 0}).sort("joiningdate", -1))
    return emps


@router.delete("/employees")
def delete_all_employees():
    result = employees.delete_many({})
    return {"message": f"Deleted {result.deleted_count} employees"}