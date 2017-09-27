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
    assert_that(context.response.status_code, equal_to(201))


@then(u'the user "{username}" exists')
def step_impl(context, username):
    data = json.loads(context.response.get_data())
    assert_that('id', is_in(data))
    user_id = data['id']
    response = context.client.get('/user/{}'.format(user_id))
    assert_that(response.status_code, equal_to(200))
    data = json.loads(response.get_data())
    assert_that('username', is_in(data))
    assert_that(data['username'] == 'charles')
    assert_that('secret', is_in(data))


@then(u'user with username "{username}" does not exist')
def step_impl(context, username):
    response = context.client.get('/user?username={}'.format(username))
    assert_that(response.status_code, equal_to(404))


@when(u'I request user with username "{username}"')
def step_impl(context, username):
    context.response = context.client.get('/user?username={}'.format(username))


@when(u'I do an injection')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I do an injection')
