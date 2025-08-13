import requests


def register(data: dict) -> requests.Response:
    return requests.post('http://127.0.0.1:5000/api/v1/register', json=data)

def login(data: dict) -> requests.Response:
    return requests.post('http://127.0.0.1:5000/api/v1/login', json=data)


def get_advertisement(aid: int) -> requests.Response:
    return requests.get(f'http://127.0.0.1:5000/api/v1/advertisements/{aid}')

def post_advertisement(data: dict, token: str = None) -> requests.Response:
    if token:
        return requests.post(
            'http://127.0.0.1:5000/api/v1/advertisements',
            headers={'Authorization': 'Bearer ' + token},
            json=data
        )
    else:
        return requests.post(
            'http://127.0.0.1:5000/api/v1/advertisements',
            json=data
        )

def patch_advertisement(aid: int, data: dict, token: str = None) -> requests.Response:
    if token:
        return requests.patch(
            f'http://127.0.0.1:5000/api/v1/advertisements/{aid}',
            headers={'Authorization': 'Bearer ' + token},
            json=data
        )
    else:
        return requests.patch(
            f'http://127.0.0.1:5000/api/v1/advertisements/{aid}',
            json=data
        )

def delete_advertisement(aid, token: str = None) -> requests.Response:
    if token:
        return requests.delete(
            f'http://127.0.0.1:5000/api/v1/advertisements/{aid}',
            headers={'Authorization': 'Bearer ' + token}
        )
    else:
        return requests.delete(
            f'http://127.0.0.1:5000/api/v1/advertisements/{aid}'
        )
