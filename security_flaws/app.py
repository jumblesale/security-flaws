from flask import Flask, make_response, abort, request
import json
import security_flaws.db as db
from security_flaws.user import create_user_from_dict


app = Flask(__name__)


@app.route('/user', methods=['POST'])
def create_user():
    data = parse_request_data(request)
    try:
        user = create_user_from_dict(data)
        saved_user = db.save_user(user)
    except ValueError as err:
        return create_json_response({'errors': err.args}, 400)
    return create_json_response(saved_user.__dict__, 201)


@app.route('/user', methods=['GET'])
def get_user():
    user_id = int(request.args.get('id'))
    if user_id is None:
        return create_json_response({'errors': ['provide a user id']}, 404)
    user = db.find_user_by_id(user_id)
    if user is None:
        return create_json_response(
            {'errors': ['user with id {}'.format(user_id)]}, 404
        )
    return create_json_response(user.__dict__, 200)


def create_json_response(payload, status_code):
    response = make_response(json.dumps(payload), status_code)
    response.headers['mimetype'] = 'application/json'
    return response


def parse_request_data(rq):
    try:
        data = rq.get_data()
        if data == b'':
            return {}
        return json.loads(data)
    except Exception:
        return {}
