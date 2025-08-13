from typing import Callable

import jwt
from aiohttp import web
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

import config
import crud
import db
import models
import views
from errors import HttpError


# noinspection PyUnusedLocal
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
                user = await crud.get(models.User, data['uid'])
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


# noinspection PyUnusedLocal,PyShadowingNames
async def close_database(app):
    await db.close()


app = web.Application(middlewares=[user_middleware, error_middleware])
app.on_cleanup.append(close_database)

app.add_routes([
    web.post('/api/v1/register', views.register),
    web.post('/api/v1/login', views.login),
    web.post('/api/v1/advertisements', views.post_advertisement),
    web.get('/api/v1/advertisements/{id:\\d+}', views.get_advertisement),
    web.patch('/api/v1/advertisements/{id:\\d+}', views.patch_advertisement),
    web.delete('/api/v1/advertisements/{id:\\d+}', views.delete_advertisement),
])
