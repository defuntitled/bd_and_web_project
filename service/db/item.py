import enum
import sqlalchemy
from sqlalchemy import orm
from service.db.db_session import SqlalchemyBase
from datetime import datetime


class TypeEnum(enum.Enum):
    FILE = 1
    FOLDER = 2


class Item(SqlalchemyBase):
    __tablename__ = "items"
    id = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True,)
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    parentId = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.Enum(TypeEnum), nullable=False)
