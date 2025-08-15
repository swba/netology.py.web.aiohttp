# import requests

# User not found.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'username': 'test',
#     'password': 'Test'
# })
# print(response.status_code)
# print(response.json())

# Email is required.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Email is incorrect.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': '<EMAIL>',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Password doesn't include uppercase letters.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'testtest'
# })
# print(response.status_code)
# print(response.json())

# Password doesn't include lowercase letters.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'TESTTEST'
# })
# print(response.status_code)
# print(response.json())

# Password doesn't include digits.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'TestTest'
# })
# print(response.status_code)
# print(response.json())

# Password is too short.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'Test123'
# })
# print(response.status_code)
# print(response.json())

# Successful registration.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# User exists.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test',
#     'email': 'test@test.com',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Username incorrect.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'username': 'test1',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Password incorrect.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'username': 'test',
#     'password': 'Test12345'
# })
# print(response.status_code)
# print(response.json())

# Successful login with username.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'username': 'test',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Successful login with email.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'email': 'test@test.com',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())
# token = response.json()['token']
# print(token)

# Anonymous attempt to create an advertisement.
# response = requests.post('http://127.0.0.1:8080/api/v1/advertisements', json={
#     'title': 'Test',
#     'description': 'Test, test and test.'
# })
# print(response.status_code)
# print(response.text)

# Attempt to create an advertisement with incorrect token.
# response = requests.post('http://127.0.0.1:8080/api/v1/advertisements', headers={
#    'Authorization': 'Bearer ' + token + '!'
# }, json={
#     'title': 'Test',
#     'description': 'Test, test and test.'
# })
# print(response.status_code)
# print(response.text)

# Attempt to create an advertisement without title.
# response = requests.post('http://127.0.0.1:8080/api/v1/advertisements', headers={
#    'Authorization': 'Bearer ' + token
# }, json={
#     'description': 'Test, test and test.'
# })
# print(response.status_code)
# print(response.json())

# Attempt to create an advertisement without description.
# response = requests.post('http://127.0.0.1:8080/api/v1/advertisements', headers={
#    'Authorization': 'Bearer ' + token
# }, json={
#     'title': 'Test',
# })
# print(response.status_code)
# print(response.json())

# Successful advertisement creation.
# response = requests.post('http://127.0.0.1:8080/api/v1/advertisements', headers={
#    'Authorization': 'Bearer ' + token
# }, json={
#     'title': 'Test',
#     'description': 'Test, test and test.',
# })
# print(response.status_code)
# print(response.json())

# Anonymously fetch an advertisement.
# response = requests.get('http://127.0.0.1:8080/api/v1/advertisements/1')
# print(response.status_code)
# print(response.json())

# Attempt to fetch a missing advertisement.
# response = requests.get('http://127.0.0.1:8080/api/v1/advertisements/666')
# print(response.status_code)
# print(response.json())

# Attempt to anonymously update an advertisement.
# response = requests.patch('http://127.0.0.1:8080/api/v1/advertisements/1', json={
#     'title': 'test1',
# })
# print(response.status_code)
# print(response.text)

# Attempt to register a new user with the same email.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test2',
#     'email': 'test@test.com',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Register a new user.
# response = requests.post('http://127.0.0.1:8080/api/v1/register', json={
#     'username': 'test2',
#     'email': 'test2@test.com',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())

# Successful login.
# response = requests.post('http://127.0.0.1:8080/api/v1/login', json={
#     'username': 'test2',
#     'password': 'Test1234'
# })
# print(response.status_code)
# print(response.json())
# token2 = response.json()['token']
# print(token2)

# Attempt to update an advertisement under another user.
# response = requests.patch('http://127.0.0.1:8080/api/v1/advertisements/1', headers={
#     'Authorization': 'Bearer ' + token2
# }, json={
#     'title': 'test1',
# })
# print(response.status_code)
# print(response.json())

# Attempt to delete an advertisement under another user.
# response = requests.delete('http://127.0.0.1:8080/api/v1/advertisements/1', headers={
#     'Authorization': 'Bearer ' + token2
# })
# print(response.status_code)
# print(response.json())

# Update an advertisement.
# response = requests.patch('http://127.0.0.1:8080/api/v1/advertisements/1', headers={
#     'Authorization': 'Bearer ' + token
# }, json={
#     'title': 'test1',
# })
# print(response.status_code)
# print(response.json())

# Check that the advertisement was updated.
# response = requests.get('http://127.0.0.1:8080/api/v1/advertisements/1')
# print(response.status_code)
# print(response.json())

# Delete an advertisement.
# response = requests.delete('http://127.0.0.1:8080/api/v1/advertisements/1', headers={
#     'Authorization': 'Bearer ' + token
# })
# print(response.status_code)
# print(response.json())

# Check that the advertisement was deleted.
# response = requests.get('http://127.0.0.1:8080/api/v1/advertisements/1')
# print(response.status_code)
# print(response.json())
