import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Orders(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    tel = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    addresses = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    order = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    payment = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)