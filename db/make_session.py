from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def create_session(engine):
    engine = create_engine(engine)
    session = Session(bind=engine)

    return session