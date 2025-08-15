import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import BaseModel
from tests import config

engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def init_database():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    yield
    engine.dispose()
