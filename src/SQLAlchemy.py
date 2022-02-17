from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
at = '@'
colon = ':'
slash = '/'
mysql = 'mysql+mysqlconnector://'

class SourceSqlalchemy(Session):
    session_factory = None
    base = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls.session_factory is None:
            # For localhost
            DB_HOST = "localhost"
            DB_PASSWORD = "NewPassword"
            DB_USER = "root"
            SCHEMA_NAME = "GOMARK_ONEMIN_TICK_DATA"
            db_url = mysql + DB_USER + colon + \
                     DB_PASSWORD + \
                     at + DB_HOST + colon + \
                     '3306' + slash + SCHEMA_NAME

            engine = create_engine(db_url, max_identifier_length=128, pool_size=20, max_overflow=100)
            cls.session_factory = sessionmaker(bind=engine, autocommit=False)
            cls.base = declarative_base(bind=engine)

            return cls.session_factory(), engine
        else:
            return cls.session_factory(), cls.session_factory().get_bind()


class TargetSqlalchemy(Session):
    session_factory = None
    base = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls.session_factory is None:
            # For localhost
            DB_HOST = "localhost"
            DB_PASSWORD = "NewPassword"
            DB_USER = "root"
            SCHEMA_NAME = "GOMARK_ONEMIN_TICK_DATA"
            db_url = mysql + DB_USER + colon + \
                     DB_PASSWORD + \
                     at + DB_HOST + colon + \
                     '3306' + slash + SCHEMA_NAME

            engine = create_engine(db_url, max_identifier_length=128, pool_size=20, max_overflow=100)
            cls.session_factory = sessionmaker(bind=engine, autocommit=False)
            cls.base = declarative_base(bind=engine)

            return cls.session_factory(), engine
        else:
            return cls.session_factory(), cls.session_factory().get_bind()
