import jwt
from rest_framework import authentication, exceptions,status

from django.conf import settings
from django.contrib.auth.models import User
# from .base_import import *
from rest_framework.response import Response
from rest_framework.views import APIView
# class JWTAuthentication(APIView):

def CheckAuth(request):
    print(request)
    try:
        if ('Authorization' in request.headers) and (len(request.headers['Auth']) != 0):
            pass
        else:
            raise exceptions.AuthenticationFailed({'error': {'code':'AUTHENTICATION_FAILURE','message':'You are not authorized to perform this operation. '}})

        auth_data = request.headers['Authorization']
        if not auth_data:
            raise exceptions.AuthenticationFailed({'error': {'code':'INVALID_HEADER_FORMAT','message':'you must be passed as authorization header '}})
        if "Bearer " not in auth_data:
            raise exceptions.AuthenticationFailed({'error': {'code':'INVALID_TOKEN_FORMAT','message':'check the token format '}})
        auth_data = auth_data.split(' ')[1]


    except IndexError as e:
        return Response({'error':{'message':e}})

    try:
        print(settings.JWT_SECRET_KEY,'==========secret-key===========')
        payload = jwt.decode(auth_data, str(settings.JWT_SECRET_KEY), algorithms="HS256")
        payload_email = payload['email']
        user = User.objects.get(username=payload_email)
        return 1

    except jwt.DecodeError as identifier:
        raise exceptions.AuthenticationFailed({'error': {"code": "AUTHENTICATION_FAILURE",'message':'You token is not valid'}})
    except jwt.ExpiredSignatureError as identifier:
        raise exceptions.AuthenticationFailed({'error': {"code": "AUTHENTICATION_FAILURE",'message':'token expired!,enter valid token'}})
    
