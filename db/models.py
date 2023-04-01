from sqlalchemy.dialects.mysql import INTEGER, TINYTEXT, TINYINT, VARCHAR, DATETIME, TEXT
from sqlalchemy import Column, ForeignKey
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