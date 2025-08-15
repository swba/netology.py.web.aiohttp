from typing import Callable

import jwt
from aiohttp import web
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

import config
import db
import models
import views
from crud import Crud
from errors import HttpError


# noinspection PyUnusedLocal,PyShadowingNames
async def orm_context(app: web.Application):
    await db.create_tables(models.BaseModel)
    yield
    await db.close()


@web.middleware
async def crud_middleware(request: web.Request, handler: Callable):
    """Adds a CRUD manager to the request."""
    async with db.SessionMaker() as session:
        request['crud'] = Crud(session)
        return await handler(request)

@web.middleware
async def user_middleware(request: web.Request, handler: Callable):
    """Authorizes a request by parsing authorization JWT."""
    user = None
    token: str = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.removeprefix('Bearer ')
        try:
            data = jwt.decode(token, key=config.SECRET_KEY, algorithms=['HS256'])
            if 'uid' in data:
                user = await request['crud'].get(models.User, data['uid'])
        except (jwt.PyJWTError, NoResultFound, MultipleResultsFound):
            pass
    request['user'] = user
    return await handler(request)

@web.middleware
async def error_middleware(request: web.Request, handler: Callable):
    """Handles errors raised by views."""
    try:
        return await handler(request)
    except HttpError as error:
        response = web.json_response({
            'status': 'error',
            'message': error.message
        })
        response.set_status(error.status_code)
        return response


app = web.Application(middlewares=[
    crud_middleware,
    user_middleware,
    error_middleware
])
app.cleanup_ctx.append(orm_context)

app.add_routes([
    web.post('/api/v1/register', views.register),
    web.post('/api/v1/login', views.login),
    web.post('/api/v1/advertisements', views.AdvertisementView),
    web.get(r'/api/v1/advertisements/{id:\d+}', views.AdvertisementView),
    web.patch(r'/api/v1/advertisements/{id:\d+}', views.AdvertisementView),
    web.delete(r'/api/v1/advertisements/{id:\d+}', views.AdvertisementView),
])


if __name__ == '__main__':
    web.run_app(app)
