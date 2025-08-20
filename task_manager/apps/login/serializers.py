import jwt
import datetime
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from apps.users_management.models import UserManagement


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Find user
        try:
            user = UserManagement.objects.get(
                username=username,
                is_active=True,
                is_deleted=False
            )
        except UserManagement.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        # Check password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password")

        # Generate tokens manually
        payload = {
            "user_id": user.id,   # DRF expects this, not "id"
            "username": user.username,
            "email": user.email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_payload = {
            "user_id": user.id,   #  again user_id
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
        }

        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")


        return {
            "access": access_token,
            "refresh": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
            },
        }
