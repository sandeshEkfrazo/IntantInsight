from typing import Optional
from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class RoleAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAccessControl
        fields = '__all__'

# class CustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'



class CustomUserSerializer(serializers.ModelSerializer):
    role_access = RoleAccessSerializer(read_only=False, allow_null=True)
    class Meta:
        model = CustomUser
        fields = ['username' ,'first_name' ,'last_name' ,'email' ,'phone_number' ,'password' ,'isAdmin' ,'create_timestamp' ,'last_update_timestamp' ,'company', 'role_access']
        
        

        




        
   

  

    


        

        

       
        
