from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class UsernameJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            username = validated_token['username']
        except KeyError:
            raise InvalidToken('Token contained no recognizable username')

        user = User.objects.get(username=username)
        if not user.is_active:
            raise AuthenticationFailed('User is inactive', code='user_inactive')
        return user
