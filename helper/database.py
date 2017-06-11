from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import DATABASE_URL


class DatabaseHelper(object):
    _engine = create_engine(DATABASE_URL, pool_recycle=3600)
    _Session = sessionmaker(bind=_engine)

    @classmethod
    def session(cls):
        return cls._Session()
