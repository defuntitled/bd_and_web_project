from service.db.db_session import create_session
from service.db.item import Item
from service.db.history import History
from service.app.item_finder import find_item_by_id, find_children


def delete_item(item):
    children = find_children(item.id)
    if not children is None:
        for child in children:
            delete_item(child)
    session = create_session()
    deleted_item = session.query(Item).filter(Item.id == item.id).first()
    session.delete(deleted_item)
    history_items = session.query(History).filter(History.item_id == item.id)
    for history_item in history_items:
        session.delete(history_item)
    session.commit()


def delete_item_by_id(id: str) -> bool:
    item = find_item_by_id(id)
    if item is None:
        return False
    delete_item(item)
    return True
