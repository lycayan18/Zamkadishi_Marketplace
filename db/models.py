from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT, TINYINT, VARCHAR, DATETIME, TEXT
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
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
    characteristics = relationship('Characteristics', overlaps="Categories,products")



ProductValues = Table("product_values", Base.metadata,
                      Column("characteristics_id", INTEGER, ForeignKey("characteristics.id")),
                      Column("product_id", INTEGER, ForeignKey("products.id")),
                      Column("value", TINYTEXT))


class Characteristics(Base):
    __tablename__ = 'characteristics'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    category_id = Column(INTEGER, ForeignKey("categories.id"))
    name = Column(TINYTEXT)
    products = relationship('Products', secondary=ProductValues, backref="Categories", overlaps="Categories,products")


class Products(Base):
    __tablename__ = 'products'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(TINYTEXT)
    category_id = Column(INTEGER, ForeignKey("categories.id"))
    price = Column(INTEGER)
    photo = Column(TINYTEXT)
    count_sold = Column(TINYTEXT, default=0)
    count_on = Column(TINYTEXT, default=0)
    characteristics = relationship('Characteristics', secondary=ProductValues, backref="Categories", overlaps="Categories,products")