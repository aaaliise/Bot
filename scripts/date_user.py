import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Date_user(SqlAlchemyBase):
    __tablename__ = 'date_user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.user_id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relationship('User')
