from dateutil import parser
import datetime
from service.db.db_session import create_session
from service.db.item import Item, TypeEnum
from service.app.item_adder import datetime_valid
from service.db.history import History


def serialize_history_item(item):
    return {
        "id": item.id,
        "type": "FILE" if item.type == TypeEnum.FILE else "FOLDER",
        "date": item.date,
        "url": item.url,
        "size": item.size,
    }


def convert_datetime(date):
    return parser.parse(date)


def check_date_for_interval(date_to_check: str, begin, end):
    return begin <= convert_datetime(date_to_check) <= end


def get_last_day_updates(date):
    if not datetime_valid(date):
        raise ValueError("unexpected date-time format")
    session = create_session()
    items = session.query(Item).filter(Item.type == TypeEnum.FILE)
    result = []
    for item in items:
        if check_date_for_interval(item.date, convert_datetime(date),
                                   convert_datetime(date) - datetime.timedelta(hours=24)):
            result.append(serialize_history_item(item))
    return result


def create_history_record(item):
    history_record = History(id=item.id, update_timestamp=item.date, item=serialize_history_item(item), )
    session = create_session()
    session.add(history_record)


def get_item_history_by_id(item_id, start_time, end_time):
    if not datetime_valid(start_time) or not datetime_valid(end_time):
        raise ValueError
    begin = convert_datetime(start_time)
    end = convert_datetime(end_time)
    if end < begin:
        raise ValueError
    session = create_session()
    history = session.query(History).filter(History.item_id == item_id)
    if history is None:
        raise KeyError
    result = []
    for record in history:
        if check_date_for_interval(record.update_timestamp, begin, end):
            result.append(record.item)
    return result
