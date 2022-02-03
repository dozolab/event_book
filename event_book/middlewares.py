import jwt
from aiohttp_jwt import JWTMiddleware, check_permissions, match_any

sharable_secret = "secret"

jwt_middleware = JWTMiddleware(
    sharable_secret,
    whitelist=[r"/login"],
    algorithms=['HS256']
)
