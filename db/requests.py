from db.models import Users, Products, Categories, Characteristics, ProductValues
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


def get_characteristics(session: Session, category_id):
    return session.query(Characteristics.name).filter(Characteristics.category_id == category_id).all()


def get_product_characteristics(session: Session, product_id):
    return session.query(Characteristics.name, ProductValues.c.value).join(Characteristics).filter(ProductValues.c.product_id == product_id).all()


def get_product(session: Session, product_id):
    return session.query(Products.name).filter(Products.id == product_id).all()