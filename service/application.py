import json

import flask
from flask import Flask, request, jsonify
from service.db.db_session import global_init
from service.app.item_finder import get_item_by_id, get_root
from service.app.item_adder import import_items
from service.app.item_deletter import delete_item_by_id
from service.app.history_worker import get_last_day_updates, get_item_history_by_id
import sys

sys.path.append('path')

app = Flask(__name__)
database_loaded = False
DB_URL = "../database/nodes.sqlite3"


def bad_answer(code: int, message: str):
    return {
        "code": code,
        "message": message
    }, str(code)


@app.route('/nodes/<string:id>', methods=["GET"])
def get_node(id: str):
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    res = get_item_by_id(id)
    if not res:
        flask.abort(404)
    else:
        return res, "200"


@app.route('/imports', methods=["POST"])
def import_nodes():
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    try:
        content = json.loads(request.get_data(as_text=True))
        if not content:
            flask.abort(400)
    except TypeError:
        flask.abort(400)
    res = import_items(content)
    if res:
        return "200"
    else:
        flask.abort(400)


@app.route("/delete/<string:id>", methods=["DELETE"])
def delete_node(id):
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    res = delete_item_by_id(id)
    if not res:
        flask.abort(404)
    return "200"


@app.route("/updates", methods=["GET"])
def get_updates():
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    date = request.args.get("date")
    if not date:
        flask.abort(400)
    try:
        return jsonify(get_last_day_updates(date)), "200"
    except ValueError:
        flask.abort(400)


@app.route("/node/<string:id_>/history")
def get_history(id_):
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    begin = request.args.get("dateStart")
    end = request.args.get("dateEnd")
    if not begin or not end:
        flask.abort(400)
    try:
        return jsonify(get_item_history_by_id(id_, begin, end)), "200"
    except ValueError:
        flask.abort(400)
    except KeyError:
        flask.abort(404)


@app.route("/nodes/root")
def get_tree_root():
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    try:
        return get_root(), "200"
    except ValueError:
        flask.abort(400)
    except KeyError:
        flask.abort(404)


@app.errorhandler(400)
def invalid_data(error):
    return bad_answer(400, "Validation Failed")


@app.errorhandler(404)
def not_found(error):
    return bad_answer(404, "Item not found")


@app.errorhandler(500)
def bad_situation(error):
    return bad_answer(400, "Validation Failed")


def run_app():
    global database_loaded
    if not database_loaded:
        global_init(DB_URL)
        database_loaded = True
    app.run(port=8080)


if __name__ == '__main__':
    run_app()
