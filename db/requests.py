from db.models import Users, Products, CategoryType, Categories, Characteristics, ProductValues, Basket, BasketHistory
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, select, and_
import sqlalchemy
import datetime


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
    return session.query(Basket.c.product_id, Basket.c.count,).filter(Basket.c.user_id == user_id).all()


def get_user_history_basket(session: Session, user_id):
    return session.query(Products.name, BasketHistory.c.count).join(Products)\
        .filter(BasketHistory.c.user_id == user_id).all()


def get_products_by_category(session, category_id):
    return session.query(Products).filter(Products.category_id == category_id).all()


def get_products_characteristics(session, product_id):
    return session.query(Characteristics.name, ProductValues.c.value).join(Characteristics)\
        .filter(ProductValues.c.product_id == product_id).all()


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


def get_category_filters(session, category_id):
    characteristics = get_characteristics(session, category_id)
    ans = []
    for i in characteristics:
        elem = [i.name]
        elem.append(list(set(i[0] for i in session.query(ProductValues.c.value)
                             .filter(ProductValues.c.characteristics_id == i.id).all())))
        elem.append(i.id)
        ans.append(elem)
    return ans


def get_product_by_name(session, name):
    return session.query(Products).filter(Products.name.like(f"%{name}%")).first()


def check_product_in_basket(session, user_id, product_id,):
    if session.query(Basket).filter(Basket.c.product_id == product_id).filter(Basket.c.user_id == user_id).count() == 0:
        query = (
                insert(Basket).
                values(user_id=user_id, product_id=product_id, count=1)
            )
    
        session.execute(query)
        session.commit()
        return False
    return True


def add_plus_product_to_basket(session, user_id, product_id):
    if check_product_in_basket(session, user_id, product_id):
        query = (
            update(Basket).
            filter(Basket.c.product_id == product_id, Basket.c.user_id == user_id).
            values(count=Basket.c.count + 1)
        )

        session.execute(query)
        session.commit()


def add_minus_product_to_basket(session, user_id, product_id):
    if check_product_in_basket(session, user_id, product_id):
        query = (
            update(Basket).
            filter(Basket.c.product_id == product_id, Basket.c.user_id == user_id).
            values(count=Basket.c.count - 1)
        )
        session.execute(query)
        session.commit()

        stmt = (
            delete(Basket).
            filter(Basket.c.count == 0)
        )

        session.execute(stmt)
        session.commit()


def add_basket_to_history(session, user_id):
    time = str(datetime.datetime.now())
    for i in session.query(Basket).filter(Basket.c.user_id == user_id).all():
        stmt = (
            insert(BasketHistory).
            values(user_id=i[0], product_id=i[1], count=i[2], date=time)
        )

        session.execute(stmt)
        session.commit()

    query = (
        delete(Basket).
        where(Basket.c.user_id == user_id)
    )

    session.execute(query)
    session.commit()


def add_product(session, name, category_id, price, filename, user_ipp, form):
    product = Products(
        name=name,
        category_id=category_id,
        price=price,
        user_ipp=user_ipp
    )

    session.add(product)
    session.commit()

    query = (
        update(Products).
        filter(Products.id == product.id).
        values(photo=filename, user_ipp=user_ipp)
    )

    session.execute(query)
    session.commit()

    for i in session.query(Characteristics.id).filter(Characteristics.category_id == category_id).all():
        query = (
            insert(ProductValues).
            values(characteristics_id=i[0], product_id=product.id, value=form.get(str(i[0])))
        )

        session.execute(query)
        session.commit()


# get_products_by_filters(session, (1, 2), ("6.7", "3200"))
def get_products_by_filters(session, category_id, characteristics_id, productvalues, price_from=0, price_to=10**10):
    if len(characteristics_id) == 0:
        stmt = (
            select(Products).
            where(Products.category_id == category_id, and_(Products.price >= price_from, Products.price <= price_to))
        )
    else:
        stmt = (
            select(Products).
            join(ProductValues).join(Characteristics).
            where(Products.category_id == category_id, ProductValues.c.characteristics_id.in_(characteristics_id),
                  ProductValues.c.value.in_(productvalues),
                  and_(Products.price >= price_from, Products.price <= price_to)).
            group_by(Products.id).
            having(sqlalchemy.func.count(Products.id) == len(characteristics_id))
        )

    return [i[0] for i in session.execute(stmt).all()]
