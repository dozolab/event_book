import json

import jwt
from aiohttp import web
from . import db
import datetime
from . import settings
from . import middlewares
from .middlewares import sharable_secret


async def person_list(request):
    async with request.app['db'].acquire() as conn:
        person = await db.get_person_list(conn=conn)
        person = [dict(q) for q in person]
        return web.Response(text=json.dumps(person))


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.date):
            return (str(z))
        else:
            return super().default(z)


async def event_list(request):
    async with request.app['db'].acquire() as conn:
        event = await db.get_event_list(conn=conn)
        event = [dict(q) for q in event]
        return web.Response(text=json.dumps(event, cls=DateTimeEncoder))


async def coupon_list(request):
    async with request.app['db'].acquire() as conn:
        event = await db.get_coupon_list(conn=conn)
        event = [dict(q) for q in event]
        return web.Response(text=json.dumps(event, cls=DateTimeEncoder))


async def login(request):
    if request.method == 'POST':
        data = await request.json()
        try:
            username = data['username']
            password = data['password']
        except (KeyError, TypeError, ValueError) as e:
            raise web.HTTPBadRequest(
                text='You have not specified username and password value') from e
        if username == settings.default_username and password == settings.default_pas:
            client_token = jwt.encode({"username": username, "password": password}, sharable_secret, algorithm="HS256")
            return web.Response(text=json.dumps({"client_token": str(client_token)}), status=201)
        return web.Response(text=json.dumps({"error": "wrong credintials"}), status=403)
    else:
        return web.Response(text=json.dumps({"error": "Get method is not allowed"}), status=400)
