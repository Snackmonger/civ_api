
from sqlalchemy import create_engine
from databases.sqlalchemy_models import Base
from databases.config import test_db



use_db = test_db

engine = create_engine(use_db, echo=False)


def init() -> None:
    Base.metadata.create_all(engine)

