from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT, TINYINT, VARCHAR, DATETIME, TEXT
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.base import Base
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


Basket = Table("basket", Base.metadata,
               Column("user_id", INTEGER, ForeignKey("users.id")),
               Column("product_id", INTEGER, ForeignKey("products.id")),
               Column("count", INTEGER, default=0))


BasketHistory = Table("basket_history", Base.metadata,
               Column("user_id", INTEGER, ForeignKey("users.id")),
               Column("product_id", INTEGER, ForeignKey("products.id")),
               Column("date", DATETIME),
               Column("count", INTEGER, default=0))


ProductValues = Table("product_values", Base.metadata,
                      Column("characteristics_id", INTEGER, ForeignKey("characteristics.id")),
                      Column("product_id", INTEGER, ForeignKey("products.id")),
                      Column("value", TINYTEXT))


class Users(Base, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    login = Column(TINYTEXT)
    password = Column(TINYTEXT)
    user_type = Column(TINYTEXT)
    user_name = Column(TINYTEXT)
    ipp = Column(TINYTEXT)


class CategoryType(Base):
    __tablename__ = "category_type"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    photo = Column(TINYTEXT)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    photo = Column(TINYTEXT)
    characteristics = relationship('Characteristics', overlaps="Categories.products")
    category_type_id = Column(INTEGER, ForeignKey("category_type.id"))


class Characteristics(Base):
    __tablename__ = 'characteristics'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    category_id = Column(INTEGER, ForeignKey("categories.id"))
    name = Column(TINYTEXT)


class Products(Base):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    category_id = Column(INTEGER, ForeignKey("categories.id"))
    price = Column(INTEGER)
    photo = Column(TINYTEXT)
    count_sold = Column(TINYTEXT, default=0)
    count_on = Column(TINYTEXT, default=0)
    characteristics = relationship('Characteristics', secondary=ProductValues, overlaps="Categories.products")
