from database.base import Base
from database.db import engine

import models.department
import models.employee
import models.equipment
import models.record
import models.user

def init_db():
    Base.metadata.create_all(engine)