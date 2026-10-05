from fastapi import FastAPI
from routers.departments import router as department_router
from routers.employees import router as employee_router
from routers.equipments import router as equipment_router
from routers.records import router as record_router
from routers.users import router as user_router
from routers.auth import router as auth_router

app = FastAPI()
app.include_router(department_router)
app.include_router(employee_router)
app.include_router(equipment_router)
app.include_router(record_router)
app.include_router(user_router)
app.include_router(auth_router)