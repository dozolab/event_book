from aiohttp import web
from event_book.db import pg_context
from event_book.routes import setup_routes
from .middlewares import *


async def init_app(argv=None):
    app = web.Application(
        middlewares=[
            jwt_middleware,
        ]
    )
    app.cleanup_ctx.append(pg_context)
    setup_routes(app)
    return app


app = init_app
