from service.db.item import TypeEnum
from datetime import datetime
import queue
from service.db.db_session import create_session
from service.db.item import Item
from service.app.history_worker import create_history_record


def deserialize_item(item: dict) -> Item:
    return Item(id=item["id"],
                type=TypeEnum.FILE if item["type"] == "FILE" else TypeEnum.FOLDER,
                url=item["url"] if item["type"] == "FILE" else None,
                size=int(item["size"]) if item["type"] == "FILE" else None,
                parentId=item["parentId"] if "parentId" in item.keys() and item["parentId"] != "null" else None
                )


def update_items(cur_id, update_date):
    q = queue.Queue()
    q.put(cur_id)
    used = set()
    session = create_session()
    while not q.empty():
        id_ = q.get()
        used.add(id_)
        updated_item = session.query(Item).filter(Item.id == id_).first()
        if updated_item is not None:
            updated_item.date = update_date
            session.commit()
        if updated_item is not None and updated_item.parentId is not None and updated_item.parentId not in used:
            q.put(updated_item.parentId)
            used.add(updated_item.parentId)


def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True


def validate_item(item: dict) -> bool:
    if item["id"] == "null":
        return False
    if item["type"] == "FOLDER" and "url" in item.keys() and item["url"] != "null":
        return False
    if item["type"] == "FILE" and len(item["url"]) > 255:
        return False
    if item["type"] == "FOLDER" and "size" in item.keys() and item["size"] != "null":
        return False
    if item["type"] == "FILE" and int(item["size"]) <= 0:
        return False
    session = create_session()
    parent = session.query(Item).filter(Item.id == item["parentId"])
    for p in parent:
        if p.type == TypeEnum.FILE:
            return False
    return True


def validate_items(content: dict) -> bool:
    if not datetime_valid(content["updateDate"]):
        return False
    items = content["items"]
    if len(items) != len(set([i["id"] for i in items])):
        return False
    for item in items:
        if not validate_item(item):
            return False
        for i in items:
            if i["id"] == item["parentId"] and i["type"] == "FILE":
                return False
    return True


def import_items(content: dict):
    if not validate_items(content):
        return False
    session = create_session()
    for it in content["items"]:
        item = deserialize_item(it)
        old_items = session.query(Item).filter(Item.id == item.id)
        for old_item in old_items:
            create_history_record(old_item,content["updateDate"])
            old_item.id = item.id
            old_item.url = item.url
            old_item.size = item.size
            old_item.type = item.type
            old_item.parentId = item.parentId
            update_items(old_item.id, content["updateDate"])
            session.commit()
        if not old_items.first():
            item.date = content["updateDate"]
            session.add(item)
            session.commit()
            update_items(item.id, content["updateDate"])
    return True
