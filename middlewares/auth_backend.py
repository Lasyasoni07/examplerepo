from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser

class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        user_id = request.session.get("user_id")
        if user_id:
            return AuthCredentials(["authenticated"]), SimpleUser(user_id)
        return AuthCredentials(["anonymous"]), SimpleUser("Anonymous")
