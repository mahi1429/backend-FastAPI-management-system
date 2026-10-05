from getpass import getpass

from sqlalchemy.exc import SQLAlchemyError

from database.db import LocalSession
from database.init_db import init_db
from models.user import User, UserRole
from schemas.user import CreateUser
from security.utils import pass_hash


def main():
    init_db()
    db = LocalSession()
    try:
        if db.query(User).first() is not None:
            raise SystemExit("Bootstrap refused: the database already contains users.")

        email = input("Initial HR email: ").strip()
        username = input("Initial HR username: ").strip()
        password = getpass("Initial HR password: ")
        password_confirmation = getpass("Confirm password: ")
        if password != password_confirmation:
            raise SystemExit("Passwords do not match.")

        account = CreateUser(
            email=email,
            username=username,
            password=password,
            role=UserRole.HR,
        )
        user = User(
            email=account.email,
            username=account.username,
            password=pass_hash(account.password),
            role=UserRole.HR.value,
        )
        db.add(user)
        db.commit()
        print(f"Created initial HR account: {user.username} ({user.id})")
    except SQLAlchemyError as exc:
        db.rollback()
        raise SystemExit("Could not create the initial HR account.") from exc
    finally:
        db.close()


if __name__ == "__main__":
    main()