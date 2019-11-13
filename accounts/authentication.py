from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        if not Token.objects.filter(uid=uid).exists():
            return None
        token = Token.objects.get(uid=uid)
        try:
            user = ListUser.objects.get(email=token.email)
            return user
        except ListUser.DoesNotExist:
            return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
