from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from config.db import db_url


class SourceSqlalchemy(Session):
    session_factory = None
    base = declarative_base()

    def __new__(cls, *args, **kwargs):
        if cls.session_factory is None:
            # For localhost
            engine = create_engine(db_url)
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
            engine = create_engine(db_url)
            cls.session_factory = sessionmaker(bind=engine, autocommit=False)
            cls.base = declarative_base(bind=engine)

            return cls.session_factory(), engine
        else:
            return cls.session_factory(), cls.session_factory().get_bind()
