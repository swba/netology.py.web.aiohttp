from functools import cache

import requests

from .api import (
    login,
    register,
    post_advertisement,
    get_advertisement,
    patch_advertisement,
    delete_advertisement
)


def test_login_not_found():
    response = login({
        'username': 'test',
        'password': 'Test'
    })
    assert response.status_code == 404
    assert response.json() == {'message': 'User with username=test not found', 'status': 'error'}

def test_register_email_required():
    response = register({
        'username': 'test',
        'password': 'Test1234'
    })
    assert response.status_code == 400
    json = response.json()
    assert json['message'][0]['loc'] == ['email']
    assert json['message'][0]['type'] == 'missing'

def test_register_email_incorrect():
    response = register({
        'username': 'test',
        'email': '<EMAIL>',
        'password': 'Test1234'
    })
    assert response.status_code == 400
    json = response.json()
    assert json['message'][0]['loc'] == ['email']
    assert json['message'][0]['type'] == 'value_error'
    assert json['message'][0]['msg'] == 'Value error, Not a valid email address.'

def assert_password_incorrect(response: requests.Response):
    assert response.status_code == 400
    json = response.json()
    assert json['message'][0]['loc'] == ['password']
    assert json['message'][0]['type'] == 'value_error'
    assert json['message'][0]['msg'] == 'Value error, Password must include at least one uppercase English letter, at least one lowercase English letter, at least one digit and be at least 8 characters long.'

def test_register_password_no_uppercase():
    response = register({
        'username': 'test',
        'email': 'test@test.com',
        'password': 'testtest'
    })
    assert_password_incorrect(response)

def test_register_password_no_lowercase():
    response = register({
        'username': 'test',
        'email': 'test@test.com',
        'password': 'TESTTEST'
    })
    assert_password_incorrect(response)

def test_register_password_no_digit():
    response = register({
        'username': 'test',
        'email': 'test@test.com',
        'password': 'TestTest'
    })
    assert_password_incorrect(response)

def test_register_password_short():
    response = register({
        'username': 'test',
        'email': 'test@test.com',
        'password': 'Test123'
    })
    assert_password_incorrect(response)

def test_register():
    response = register({
        'username': 'test',
        'email': 'test@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 200
    assert response.json() == {'id': 1}

def test_register_existing_username():
    response = register({
        'username': 'test',
        'email': 'test2@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 409
    assert response.json() == {'message': 'User already exists', 'status': 'error'}

def test_register_existing_email():
    response = register({
        'username': 'test2',
        'email': 'test@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 409
    assert response.json() == {'message': 'User already exists', 'status': 'error'}

def test_login_username_incorrect():
    response = login({
        'username': 'test1',
        'password': 'Test1234'
    })
    assert response.status_code == 404
    assert response.json() == {'message': 'User with username=test1 not found', 'status': 'error'}

def test_login_email_incorrect():
    response = login({
        'email': 'test1@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 404
    assert response.json() == {'message': 'User with email=test1@test.com not found', 'status': 'error'}

def test_login_password_incorrect():
    response = login({
        'username': 'test',
        'password': 'Test12345'
    })
    assert response.status_code == 401
    assert response.json() == {'message': 'Invalid password', 'status': 'error'}

def test_login_username():
    response = login({
        'username': 'test',
        'password': 'Test1234'
    })
    assert response.status_code == 200
    assert 'token' in response.json()

def test_login_email():
    response = login({
        'email': 'test@test.com',
        'password': 'Test1234'
    })
    assert response.status_code == 200
    assert 'token' in response.json()

@cache
def get_token() -> str:
    response = login({
        'username': 'test',
        'password': 'Test1234'
    })
    return response.json()['token']

def test_advertisement_create_anonymous():
    response = post_advertisement({
        'title': 'Test',
        'description': 'Test, test and test.'
    })
    assert response.status_code == 401
    assert response.json() == {'message': 'Unauthorized access', 'status': 'error'}

def test_advertisement_create_incorrect_token():
    response = post_advertisement({
        'title': 'Test',
        'description': 'Test, test and test.'
    }, token='TheTOKEN!')
    assert response.status_code == 401
    assert response.json() == {'message': 'Unauthorized access', 'status': 'error'}

def test_advertisement_create_no_title():
    response = post_advertisement({
        'description': 'Test, test and test.'
    }, token=get_token())
    assert response.status_code == 400
    json = response.json()
    assert json['message'][0]['loc'] == ['title']
    assert json['message'][0]['type'] == 'missing'
    assert json['message'][0]['msg'] == 'Field required'

def test_advertisement_create_no_description():
    response = post_advertisement({
        'title': 'Test',
    }, token=get_token())
    assert response.status_code == 400
    json = response.json()
    assert json['message'][0]['loc'] == ['description']
    assert json['message'][0]['type'] == 'missing'
    assert json['message'][0]['msg'] == 'Field required'

def assert_first_advertisement(response, data: dict = None):
    if data is None:
        data = {}
    assert response.status_code == 200
    json = response.json()
    assert json['id'] == 1
    assert json['title'] == data.get('title', 'Test')
    assert json['description'] == data.get('description', 'Test, test and test.')
    assert json['owner'] == {'email': 'test@test.com', 'id': 1, 'username': 'test'}

def test_advertisement_create():
    response = post_advertisement({
        'title': 'Test',
        'description': 'Test, test and test.',
    }, token=get_token())
    assert_first_advertisement(response)

def test_advertisement_get():
    response = get_advertisement(1)
    assert_first_advertisement(response)

def test_advertisement_get_missing():
    response = get_advertisement(666)
    assert response.status_code == 404
    assert response.json() == {'message': 'Advertisement with id=666 not found', 'status': 'error'}

def test_advertisement_update_anonymous():
    response = patch_advertisement(1, {
        'title': 'test1',
    })
    assert response.status_code == 401
    assert response.json() == {'message': 'Unauthorized access', 'status': 'error'}

def test_advertisement_delete_anonymous():
    response = delete_advertisement(1)
    assert response.status_code == 401
    assert response.json() == {'message': 'Unauthorized access', 'status': 'error'}

def test_advertisement_update_delete_not_owner():
    register({
        'username': 'test2',
        'email': 'test2@test.com',
        'password': 'Test1234'
    })
    response = login({
        'username': 'test2',
        'password': 'Test1234'
    })
    token2 = response.json()['token']

    response = patch_advertisement(1, {
        'title': 'test1',
    }, token=token2)
    assert response.status_code == 403
    assert response.json() == {'message': 'Only advertisement owner can edit or delete it', 'status': 'error'}

    response = delete_advertisement(1, token=token2)
    assert response.status_code == 403
    assert response.json() == {'message': 'Only advertisement owner can edit or delete it', 'status': 'error'}

def test_advertisement_update():
    response = patch_advertisement(1, {
        'title': 'Test1',
    }, token=get_token())
    assert_first_advertisement(response, {'title': 'Test1'})

def test_advertisement_get_after_update():
    response = get_advertisement(1)
    assert_first_advertisement(response, {'title': 'Test1'})

def test_advertisement_delete():
    response = delete_advertisement(1, get_token())
    assert response.status_code == 200
    assert response.json() == {'message': 'Advertisement deleted successfully'}

def test_advertisement_get_after_delete():
    response = get_advertisement(1)
    assert response.status_code == 404
    assert response.json() == {'message': 'Advertisement with id=1 not found', 'status': 'error'}
