from datetime import date

from models.department import Department
from models.equipment import Equipment
from models.user import User, UserRole
from security.utils import pass_hash


def add_user(database, *, email, role, department_id=None, password="unused"):
    with database() as db:
        user = User(
            email=email,
            username=email.split("@", maxsplit=1)[0],
            password=password,
            role=role.value,
            department_id=department_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id


def add_department(database, name):
    with database() as db:
        department = Department(name=name)
        db.add(department)
        db.commit()
        db.refresh(department)
        return department.id


def test_login_returns_bearer_token_and_token_authenticates(client, database):
    add_user(
        database,
        email="hr@example.com",
        role=UserRole.HR,
        password=pass_hash("correct-password"),
    )

    response = client.post(
        "/auth/login",
        data={"username": "hr@example.com", "password": "correct-password"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]

    departments = client.get(
        "/departments/",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )
    assert departments.status_code == 200


def test_login_rejects_invalid_password(client, database):
    add_user(
        database,
        email="hr@example.com",
        role=UserRole.HR,
        password=pass_hash("correct-password"),
    )

    response = client.post(
        "/auth/login",
        data={"username": "hr@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_only_hr_can_create_departments(client, database, auth_headers):
    add_user(database, email="hr@example.com", role=UserRole.HR)
    add_user(database, email="staff@example.com", role=UserRole.REGULAR_STAFF)

    created = client.post(
        "/departments/",
        json={"name": "Operations"},
        headers=auth_headers("hr@example.com"),
    )
    denied = client.post(
        "/departments/",
        json={"name": "Restricted"},
        headers=auth_headers("staff@example.com"),
    )

    assert created.status_code == 201
    assert created.json()["name"] == "Operations"
    assert denied.status_code == 403


def test_manager_can_only_view_their_department(client, database, auth_headers):
    own_department_id = add_department(database, "North")
    add_department(database, "South")
    add_user(
        database,
        email="manager@example.com",
        role=UserRole.MAINTENANCE_MANAGER,
        department_id=own_department_id,
    )

    departments = client.get(
        "/departments/",
        headers=auth_headers("manager@example.com"),
    )
    own_department = client.get(
        f"/departments/{own_department_id}",
        headers=auth_headers("manager@example.com"),
    )
    other_department = client.get(
        f"/departments/{own_department_id + 1}",
        headers=auth_headers("manager@example.com"),
    )

    assert departments.status_code == 200
    assert [department["id"] for department in departments.json()] == [
        own_department_id
    ]
    assert own_department.status_code == 200
    assert other_department.status_code == 403


def test_regular_staff_only_sees_assigned_equipment(client, database, auth_headers):
    department_id = add_department(database, "Operations")
    staff_id = add_user(
        database,
        email="staff@example.com",
        role=UserRole.REGULAR_STAFF,
        department_id=department_id,
    )
    with database() as db:
        assigned = Equipment(
            type="Generator",
            model="G-100",
            manufacturer="Acme",
            purchase_date=date(2024, 1, 1),
            status="active",
            department_id=department_id,
            assigned_staff_id=staff_id,
        )
        unassigned_to_user = Equipment(
            type="Pump",
            model="P-200",
            manufacturer="Acme",
            purchase_date=date(2024, 1, 1),
            status="active",
            department_id=department_id,
            assigned_staff_id="another-user-id",
        )
        db.add_all([assigned, unassigned_to_user])
        db.commit()

    response = client.get(
        "/equipments/",
        headers=auth_headers("staff@example.com"),
    )

    assert response.status_code == 200
    assert [equipment["model"] for equipment in response.json()] == ["G-100"]
