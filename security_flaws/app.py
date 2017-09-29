from flask import Flask, g, make_response, request, render_template, abort, redirect
import json
from security_flaws.user import create_user_from_dict as create_user_entity_from_dict
from security_flaws.note import create_note as create_note_entity
import security_flaws.log as log

# initialise the flask app
app = Flask(__name__)

# the db import has to come after the app gets initialised
import security_flaws.db as db


@app.route('/')
def index():
    return redirect('login')


@app.route('/user', methods=['POST'])
def create_user():
    log.log('received user creation request with data: {}'.format(request.get_data()))
    data = parse_request_data(request)
    try:
        user = create_user_entity_from_dict(data)
        if db.find_user_by_username(user.username) is not None:
            return _create_error_response(
                ['Username {} already exists'.format(user.username)]
            )
        saved_user = db.save_user_in_a_very_unsafe_way(user)
    except ValueError as err:
        return _create_error_response(err.args)
    return create_json_response(saved_user.__dict__, 201)


@app.route('/notes', methods=['POST'])
def create_note():
    log.log('received note creation request with data: {}'.format(request.get_data()))
    data = parse_request_data(request)
    from_user = db.find_user_by_username(data['from_username'])
    to_user = db.find_user_by_username(data['to_username'])
    errors = []
    if 'note' not in data:
        errors.append('No note provided')
    if from_user is None:
        errors.append('From user "{}" does not exist'.format(data['from_username']))
    if to_user is None:
        errors.append('To user "{}" does not exist'.format(data['to_username']))
    if errors:
        return _create_error_response(errors)
    note = create_note_entity(from_user, to_user, data['note'])
    saved_note = db.save_note(note)
    return create_json_response(json.dumps({
        'note': saved_note.note,
        'from_username': saved_note.from_user.username,
        'from_user_id': saved_note.from_user.id,
        'to_username': saved_note.to_user.username,
        'to_user_id': saved_note.to_user.id,
        'id': saved_note.id
    }), 201)


@app.route('/notes', methods=['GET'])
def get_note():
    username = request.args.get('username')
    if username is None:
        return create_json_response({'errors': ['Provide a username']}, 404)
    user = db.find_user_by_username(username)
    if user is None:
        return create_json_response(
            {'errors': ['User with username {} does not exist'.format(username)]}, 404
        )
    notes = db.find_notes_sent_to_user_id(user.id)
    return create_json_response({'notes': notes})


def _create_registration_error_response(errors: [str]):
    return create_json_response(
        {'errors': errors},
        400
    )


def _create_error_response(errors: [str]):
    return create_json_response(
        {'errors': errors},
        400
    )


@app.route('/users', methods=['GET'])
def get_user_by_username():
    username = request.args.get('username')
    if username is None:
        return create_json_response({'errors': ['Provide a username']}, 404)
    user = db.find_user_by_username(username)
    if user is None:
        return create_json_response(
            {'errors': ['User with username {} does not exist'.format(username)]}, 404
        )
    return create_json_response(user.__dict__, 200)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = db.find_user_by_id(user_id)
    if user is None:
        return create_json_response(
            {'errors': ['User with id {} does not exist'.format(user_id)]}, 404
        )
    return create_json_response(user.__dict__, 200)


@app.route('/login', methods=['GET'])
def register():
    return render_template('login.html', header='Log in')


@app.route('/user_page', methods=['GET'])
def user_page():
    user_id = request.args.get('id')
    user = db.find_user_by_id(user_id)
    if user is None:
        return abort(404)
    title = "{}'s user page".format(user.username)
    return render_template('user_page.html', user=user, title=title)


def create_json_response(payload, status_code=200):
    log.response(status_code, payload)
    data = json.dumps(payload)
    response = make_response(data, status_code)
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
