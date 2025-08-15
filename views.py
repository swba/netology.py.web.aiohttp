import time

import jwt
from aiohttp import web
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

import config
from crud import Crud
from errors import HttpError
from models import Advertisement, User
from validation import (
    validate_data,
    AdvertisementValidator,
    AdvertisementUpdateValidator,
    UserValidator,
    UserLoginValidator
)


async def register(request: web.Request):
    json_data = await request.json()
    data = validate_data(json_data, UserValidator)
    data['password'] = generate_password_hash(data['password'], salt_length=8)
    user = User(**data)
    try:
        await request['crud'].save(user)
    except IntegrityError:
        raise HttpError(409, f"User already exists")
    return web.json_response({'id': user.id})

async def login(request: web.Request):
    json_data = await request.json()
    data = validate_data(json_data, UserLoginValidator)
    user: User | None = None
    # Try to find user first by username and then by email.
    if 'username' in data:
        if not (user := await request['crud'].get(User, data['username'], 'username')):
            raise HttpError(404, f"User with username={data['username']} not found")
    elif 'email' in data:
        if not (user := await request['crud'].get(User, data['email'], 'email')):
            raise HttpError(404, f"User with email={data['email']} not found")
    if not check_password_hash(str(user.password), data['password']):
        raise HttpError(401, "Invalid password")
    # Generate and return JWT.
    token = jwt.encode(
        {
            'uid': user.id,
            'exp': int(time.time()) + config.TOKEN_TTL
        },
        key=config.SECRET_KEY,
        algorithm='HS256'
    )
    return web.json_response({'token': token})


class AdvertisementView(web.View):

    @property
    def crud(self) -> Crud:
        return self.request['crud']

    async def get(self):
        ad = await self._load()
        return web.json_response(ad.dict())

    async def post(self):
        _check_logged_in(self.request)

        json_data = await self.request.json()
        data = validate_data(json_data, AdvertisementValidator)

        ad = Advertisement(**data, owner=self.request['user'])
        await self.crud.save(ad)

        return web.json_response(ad.dict())

    async def patch(self):
        _check_logged_in(self.request)

        ad = await self._load()
        self._check_owner(ad)

        json_data = await self.request.json()
        data = validate_data(json_data, AdvertisementUpdateValidator)

        # Update advertisement.
        for k, v in data.items():
            setattr(ad, k, v)
        await self.crud.save(ad)

        return web.json_response(ad.dict())

    async def delete(self):
        _check_logged_in(self.request)

        ad = await self._load()
        self._check_owner(ad)

        await self.crud.delete(ad)
        return web.json_response({
            'message': "Advertisement deleted successfully"
        })

    async def _load(self) -> Advertisement:
        advertisement_id: int = int(self.request.match_info['id'])
        advertisement = await self.crud.get(Advertisement, advertisement_id)
        if not advertisement:
            raise HttpError(404, f"Advertisement with id={advertisement_id} not found")
        return advertisement

    def _check_owner(self, advertisement: Advertisement):
        if advertisement.owner != self.request['user']:
            raise HttpError(403, "Only advertisement owner can edit or delete it")


def _check_logged_in(request: web.Request):
    if not request['user']:
        raise HttpError(401, "Unauthorized access")
