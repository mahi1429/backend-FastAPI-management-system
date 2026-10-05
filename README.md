# Equipment Maintenance API

## About

The Equipment Maintenance API is a backend system for organizing equipment maintenance within a company. It manages departments, employees, user accounts, equipment, and maintenance records. Access is controlled through bearer-token authentication and role-based permissions, so users can work with the information and operations appropriate to their role. Equipment is associated with its owning department, while repair-staff assignments are tracked separately.

## Tech stack

- **Language:** Python 3.13
- **API framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Data validation and settings:** Pydantic and Pydantic Settings
- **Authentication:** JWT bearer tokens with `python-jose`
- **Password hashing:** Passlib and bcrypt
- **ASGI server:** Uvicorn

## Main capabilities

- Create and manage departments and employee records.
- Manage equipment and assign repair staff.
- Create and view maintenance records.
- Restrict API operations according to user roles.
- Explore the API through FastAPI's generated OpenAPI documentation.

## User roles

- **HR:** Creates user accounts and departments, and manages employee details.
- **Maintenance manager:** Manages equipment and repair-staff assignments, creates maintenance records, and views details for their own department.
- **Maintenance supervisor:** Views equipment and maintenance records.
- **Regular staff:** Views equipment assigned to their account.

Maintenance records do not currently have update or delete endpoints.



This project was created by me for learning purposes. It is a practice project and is not intended to be used as a production system. The JWT secret currently configured in the project is a development placeholder; do not use it for a deployed or shared application.