from db.models import Users, Products, CategoryType, Categories, Characteristics, ProductValues, Basket, BasketHistory
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
    return session.query(Characteristics).filter(Characteristics.category_id == category_id).all()


def get_product(session: Session, product_id):
    return session.query(Products.name).filter(Products.id == product_id).all()


def get_user_basket(session: Session, user_id):
    return session.query(Basket.c.product_id).filter(Basket.c.user_id == user_id).all()


def get_user_history_basket(session: Session, user_id):
    return session.query(Products.name, BasketHistory.c.count).join(Products).filter(BasketHistory.c.user_id == user_id).all()


def get_products_by_category(session, category_id):
    return session.query(Products).filter(Products.category_id == category_id).all()


def get_products_characteristics(session, product_id):
    return session.query(Characteristics.name, ProductValues.c.value).join(Characteristics).filter(ProductValues.c.product_id == product_id).all()


def get_category_type(session):
    return session.query(CategoryType).all()


def get_category_by_category_type(session, category_type_id):
    return session.query(Categories).filter(Categories.category_type_id == category_type_id).all()


def get_top_products(session):
    return session.query(Products).all()


def get_category_type_by_id(session, id):
    return session.query(CategoryType).filter(CategoryType.id == id).first()


def get_category_by_id(session, id):
    return session.query(Categories).filter(Categories.id == id).first()


def get_product_by_id(session, id):
    return session.query(Products).filter(Products.id == id).first()