from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)

        token = params.get("token")

        if token:
            try:
                access_token = AccessToken(token[0])
                user = User.objects.get(id=access_token["user_id"])
                scope["user"] = user
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)