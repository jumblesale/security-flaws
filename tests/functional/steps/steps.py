from behave import *
from security_flaws.app import app
import security_flaws.db as db
from hamcrest import assert_that, equal_to, is_in
import json


@given(u'the server is running')
def step_impl(context):
    app.config['TESTING'] = True
    context.client = app.test_client()


@given(u'I have the following request')
def step_impl(context):
    context.raw_request = context.text


@given(u'there are no existing users')
def step_impl(context):
    # this is cheating, the functional tests should not have this level
    # of access to the system
    connection = db._init_db()
    db.create_schema(connection)


@given(u'there are fixtures in the db')
def step_impl(context):
    context.execute_steps(u"""
        Given there are no existing users
    """)
    with app.app_context():
        connection = db.get_db()
        db.insert_fixtures(connection)
        db.close_connection()


@given(u'I am a client')
def step_impl(context):
    pass


@given(u'I register with username "{username}" and secret "{secret}"')
@when(u'I register with username "{username}" and secret "{secret}"')
def step_impl(context, username, secret):
    payload = json.dumps({
        'username': username,
        'secret': secret
    })
    context.response = context.client.post('/user', data=payload)


@then(u'the user "{username}" exists')
@given(u'the user "{username}" exists')
def step_impl(context, username):
    response = context.client.get('/user?username={}'.format(username))
    assert_that(response.status_code, equal_to(200))
    data = json.loads(response.get_data())
    assert_that('username', is_in(data))
    assert_that(data['username'] == 'charles')
    assert_that('secret', is_in(data))


@then(u'the user with username "{username}" does not exist')
def step_impl(context, username):
    response = context.client.get('/user?username={}'.format(username))
    assert_that(response.status_code, equal_to(404))


@when(u'I request user with username "{username}"')
def step_impl(context, username):
    context.response = context.client.get('/user?username={}'.format(username))


@given(u'I get a "{status}" response')
@then(u'I get a "{status}" response')
def step_impl(context, status):
    assert_that(context.response.status_code, equal_to(int(status)))


@given(u'I am user "{username}"')
def step_impl(context, username):
    context.username = username


@given(u'I send a note "{note}" to user "{to_username}"')
def step_impl(context, note, to_username):
    payload = json.dumps({
        'note': note,
        'to_username': to_username,
        'from_username': context.username
    })
    context.response = context.client.post('/notes', data=payload)


@then(u'that request is unsuccessful ({status})')
@then(u'that request is successful ({status})')
def step_impl(context, status):
    assert_that(context.response.status_code, equal_to(int(status)))


@then(u'user "{username}" has {count} notes')
def step_impl(context, username, count):
    context.response = context.client.get('/notes?username={}'.format(username))
    data = json.loads(context.response.get_data())
    assert_that(len(data['notes']), equal_to(int(count)))
    context.notes = data['notes']


@then(u'the first note contains "{text}"')
def step_impl(context, text):
    assert_that(context.notes[0]['note'], equal_to(text))


@when(u'I log in with username "{username}" and secret "{secret}"')
def step_impl(context, username, secret):
    payload = json.dumps({
        'username': username,
        'secret':   secret
    })
    context.response = context.client.post('/auth', data=payload)


@when(u'I request a list of users')
def step_impl(context):
    context.response = context.client.get('/users')


@then(u'I get {count} users')
def step_impl(context, count):
    data = json.loads(context.response.get_data())
    assert_that(len(data['users']), equal_to(int(count)))
