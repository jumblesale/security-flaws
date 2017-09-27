from behave import *
import security_flaws.db as db
from security_flaws.app import app
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
    db.create_schema()


@given(u'I am a client')
def step_impl(context):
    pass


@when(u'I register with username "{username}" and secret "{secret}"')
def step_impl(context, username, secret):
    payload = json.dumps({
        'username': username,
        'secret': secret
    })
    context.response = context.client.post('/user', data=payload)
    assert context.response.status_code == 201


@then(u'the user "{username}" exists')
def step_impl(context, username):
    data = json.loads(context.response.get_data())
    assert 'id' in data
    user_id = data['id']
    response = context.client.get('/user?id={}'.format(user_id))
    assert response.status_code == 200
    data = json.loads(response.get_data())
    assert 'username' in data
    assert data['username'] == 'charles'
    assert 'secret' in data
