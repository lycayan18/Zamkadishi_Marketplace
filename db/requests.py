from db.models import Users
from sqlalchemy.orm import Session

def add_user(session: Session, user_name, login, password, user_type="buyer", ipp=""):
    query = Users(
        user_name=user_name,
        ipp=ipp,
        login=login,
        password=password,
        user_type=user_type
    )

    session.add(query)
    session.commit()


def get_user_id(session: Session, login):
    return session.query(Users).filter(Users.login == login).first()


def get_user(session: Session, user_id):
    return session.query(Users).get(user_id)


def get_password(session: Session, login):
    return session.query(Users.password).filter(Users.login == login).all()