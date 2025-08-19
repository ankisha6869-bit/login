from wsgiref import validate
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserManagement

#This is where we can write serializers which will help serialize the data and add validations to the data accordingly
#Lets make a serializer for UserManagement model

class UserManagementSerializer(serializers.Serializer):
    username = serializers.CharField(required = True, max_length = 25, min_length = 3, allow_blank = False, allow_null= False)
    first_name = serializers.CharField(required = True, max_length = 35, min_length = 3, allow_blank = False, allow_null= False)
    last_name = serializers.CharField(required = True, max_length = 35, min_length = 3, allow_blank = False, allow_null= False)
    password = serializers.CharField(required = True, max_length = 35, min_length = 3, allow_blank = False, allow_null= False)
    email = serializers.EmailField(required = True,max_length=None, min_length=None, allow_blank=False)
    phone_number = serializers.IntegerField(required = True,)
    dob = serializers.DateField(required = True,)
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)
    is_deleted = serializers.BooleanField(read_only = True)
    is_active = serializers.BooleanField(read_only = True)
    
    def validate_username(self, value):
        user_qs = UserManagement.objects.filter(username=value)
        if self.instance:
            user_qs = user_qs.exclude(pk=self.instance.pk)
        if user_qs.exists():
            raise serializers.ValidationError('Username already taken')
        return value 


    def validate_phone_number(self, value):
        value = str(value)
        if len(value)<10 and len(value)>10:
            raise serializers.ValidationError('Please enter a valid phone number')
        return value

    def create(self, validated_data):
        from django.db import transaction
        try:
            with transaction.atomic():
                user = UserManagement.objects.create(
                    username = validated_data['username'],
                    first_name = validated_data['first_name'],
                    last_name = validated_data['last_name'],
                    email = validated_data['email'],
                    phone_number = validated_data['phone_number'],
                    dob = validated_data['dob'],
                    password = make_password(validated_data['password'])
                    )
        except Exception as e:
            raise serializers.ValidationError({"Error": str(e)})
        return user

    def update(self,instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.dob = validated_data.get('dob', instance.dob)

        instance.save()
        return instance

