import sqlalchemy
from service.db.db_session import SqlalchemyBase


class History(SqlalchemyBase):
    __tablename__ = "items_history"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True)
    item_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("items.id"))
    update_timestamp = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    item = sqlalchemy.Column(sqlalchemy.JSON, nullable=False)
