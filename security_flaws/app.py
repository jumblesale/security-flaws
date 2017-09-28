from flask import Flask, g, make_response, request
import json
from security_flaws.user import create_user_from_dict

# initialise the flask app
app = Flask(__name__)

import security_flaws.db as db


@app.route('/user', methods=['POST'])
def create_user():
    data = parse_request_data(request)
    try:
        user = create_user_from_dict(data)
        if db.find_user_by_username(user.username) is not None:
            return _create_registration_error_response(
                ['username {} already exists'.format(user.username)]
            )
        saved_user = db.save_user_in_a_very_unsafe_way(user)
    except ValueError as err:
        return _create_registration_error_response(err.args)
    return create_json_response(saved_user.__dict__, 201)


def _create_registration_error_response(errors: [str]):
    return create_json_response(
        {'errors': errors},
        400
    )


@app.route('/users', methods=['GET'])
def get_user():
    user_name = request.args.get('username')
    if user_name is None:
        return create_json_response({'errors': ['provide a username']}, 404)
    user = db.find_user_by_username(user_name)
    if user is None:
        return create_json_response(
            {'errors': ['user with username {}'.format(user_name)]}, 404
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


@app.teardown_appcontext
def close_connection(exception):
    connection = db.get_db()
    if db is not None:
        connection.close()
