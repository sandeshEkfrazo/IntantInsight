# from os import O_TMPFILE
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import jwt
from rest_framework import authentication, exceptions, status
from account.models import *
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from jose.constants import ALGORITHMS
from django.http import HttpRequest
from functools import wraps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# def CheckAuthData(request, *args, **kwargs):
#     print("==========================header", request.headers)
#     try:
#         if ('Authorization' in request.headers) and (len(request.headers['Authorization']) != 0):
#             pass
#             print("============", request.headers['Authorization'])
#         else:
#             raise exceptions.AuthenticationFailed(
#                     {'error': {'code': 'AUTHENTICATION_FAILURE', 'message': 'You are not authorized to perform this operation. '}})

#         auth_data = request.headers['Authorization']
#         if not auth_data:
#             raise exceptions.AuthenticationFailed(
#                 {'error': {'code': 'INVALID_HEADER_FORMAT', 'message': 'you must be passed as Authorisation header '}})
#         if "Bearer " not in auth_data:
#             raise exceptions.AuthenticationFailed(
#                 {'error': {'code': 'INVALID_TOKEN_FORMAT', 'message': 'check the token format '}})
#         auth_data = auth_data.split(' ')[1]

#     except IndexError as e:
#         return Response({'error': {'message': e}})

#     try:
#         print(settings.JWT_SECRET_KEY, '====hello======secret-key===========')
#         payload = jwt.decode(auth_data, str(
#             settings.JWT_SECRET_KEY), algorithms="HS256")
#         payload_id = payload['user_id']
#         print(payload_id)
#         user_id = CustomUser.objects.get(id=payload_id)
#         return user_id

#     except jwt.DecodeError as identifier:
#         raise exceptions.AuthenticationFailed(
#             {'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You token is not valid'}})
#     except jwt.ExpiredSignatureError as identifier:
#         raise exceptions.AuthenticationFailed(
#             {'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'token expired!,enter valid token'}})


def authorization_required(func):
    def checkAuthData(request, *args, **kwargs):
        print("request==>>header=",kwargs)
        try:
            if ('Authorization' in request.headers) and (len(request.headers['Authorization']) != 0):
                pass
            else:
                # raise exceptions.AuthenticationFailed(
                #     {'error': {'code': 'AUTHENTICATION_FAILURE', 'message': 'You are not authorized to perform this operation. '}})
                # return render(request, 'error-page.html', status=status.HTTP_401_UNAUTHORIZED) 
                return JsonResponse({'error': {'code': 'AUTHENTICATION_FAILURE', 'message': 'You are not authorized to perform this operation. '}}, status=status.HTTP_401_UNAUTHORIZED)

            auth_data = request.headers['Authorization']
            if not auth_data:
                return JsonResponse(
                    {'error': {'code': 'INVALID_HEADER_FORMAT', 'message': 'you must be passed as Auth header '}}, status=status.HTTP_401_UNAUTHORIZED)
            if "Bearer " not in auth_data:
                return JsonResponse(
                    {'error': {'code': 'INVALID_TOKEN_FORMAT', 'message': 'check the token format '}}, status=status.HTTP_401_UNAUTHORIZED)
            auth_data = auth_data.split(' ')[1]

        except IndexError as e:
            return Response({'error': {'message': e}})

        try:
            print(settings.SECRET_KEY, '======hello2====secret-key===========')
            payload = jwt.decode(auth_data, str(
                settings.JWT_SECRET_KEY), algorithms="HS256")
            payload_id = payload['user_id']
            # print("payload_id",payload_id)
            user_id = CustomUser.objects.get(id=payload_id)
            # return user_id
        except jwt.DecodeError as identifier:
            return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You token is not valid'}}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError as identifier:
            return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'token expired!,enter valid token'}}, status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)
    return checkAuthData



def Pagination(data, page_number, data_per_page,request):

    base_url = request.build_absolute_uri('?page_number')

    paginator = Paginator(data, data_per_page)
    page = paginator.page(page_number)
   
    if page.has_next():
        next_page = int(page_number) + 1
        next_url = str(base_url) + '=' + str(next_page) +'&data_per_page='+str(data_per_page)
    else:
        next_url = None

    if page.has_previous():
        previous_page = int(page_number) - 1
        previous_url = str(base_url) + '=' + str(previous_page) +'&data_per_page='+str(data_per_page)
    else:
        previous_url = None
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    pagination_object = {
        'current_page':page.number,
        'number_of_pages':paginator.num_pages,
        'next_url':next_url,
        'previous_url':previous_url,
        'next_page_number':page.next_page_number,
        'previous_page_number':page.previous_page_number,
        'has_next':page.has_next(),
        'has_previous':page.has_previous(),
        'has_other_pages':page.has_other_pages(),
    }
   
    return list(page_obj),(pagination_object)