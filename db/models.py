from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT, TINYINT, VARCHAR, DATETIME, TEXT
from sqlalchemy import Column, ForeignKey, Table
from db.base import Base
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Users(Base, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    login = Column(TINYTEXT)
    password = Column(TINYTEXT)
    user_type = Column(TINYTEXT)
    user_name = Column(TINYTEXT)
    ipp = Column(TINYTEXT)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)


#class Characteristics(Base):
#    __tablename__ = 'characteristics'
#
#    category_id = Column(INTEGER, ForeignKey("categories.id"))
#    name = Column(TINYTEXT)
Characteristics = Table('characteristics', Base.metadata,
                        Column("category_id", INTEGER, ForeignKey("categories.id")),
                        Column("name", TINYTEXT))


class Products(Base):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    category_id = Column(INTEGER, ForeignKey("categories.id"))
    price = Column(INTEGER)
    photo = Column(TINYTEXT)
    count_sold = Column(TINYTEXT, default=0)
    count_on = Column(TINYTEXT, default=0)


Basket = Table("basket", Base.metadata,
               Column("user_id", INTEGER, ForeignKey("users.id")),
               Column("product_id", INTEGER, ForeignKey("products.id")),
               Column("count", INTEGER, default=0))


BasketHistory = Table("basket_history", Base.metadata,
                      Column("user_id", INTEGER, ForeignKey("users.id")),
                      Column("product_id", INTEGER, ForeignKey("products.id")),
                      Column("date", DATETIME),
                      Column("count", INTEGER, default=0))