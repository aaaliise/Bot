import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Table2(SqlAlchemyBase):
    __tablename__ = 'money_user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user_id"))
    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user = orm.relationship('Table0')
