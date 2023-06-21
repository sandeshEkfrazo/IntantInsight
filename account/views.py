from os import stat
import re
from django.core.checks.messages import Error
from django.core.mail import EmailMessage
from django.conf import settings
import pandas as pd
from re import sub
import random
from typing import Type
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from rest_framework import views
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed

# from account.backends_ import CheckAuthData
# from numpy import add
from .serializers import *
from .models import *
from django.db.models import Q, query
from django.http import JsonResponse, response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
import string
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from datetime import timedelta, datetime
from django.conf import settings
# from jose import jwt
from jose.constants import ALGORITHMS
from jose.jwt import JWTError
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import get_template
import jwt


# print(make_password('1234'))
# print(check_password('1234','pbkdf2_sha256$260000$x4LuTvjrgmyQE7JaZnP3sZ$Dkmf78TGidy51SL8HhbeRqNcMicydK5F/xGdz7tx5UE='))

# ?-------------------------  JWT LOG-IN-------------------------------------------------------------------------------


# class LoginView(GenericAPIView):
#     serializer_class = CustomUserSerializer

#     def post(self, request):
#         response = {}
#         data = request.data
#         username = data.get('username')
#         password = data.get('password')
#         print(data)

#         user = auth.authenticate(username=username, password=password)

#         if user:
#             custom_user = CustomUser.objects.get(user_id=user.id)
#             print(custom_user)
#             auth_token = jwt.encode(
#                 {'user_id': user.id, 'username': user.username, 'email': user.email, 'phone_number': custom_user.phone_number}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

#             serializer = CustomUserSerializer(user)
#             authorization = 'Bearer'+' '+auth_token
#             response_result = {}
#             response_result['result'] = {
#                 'detail': 'Login successfull', 'status': status.HTTP_200_OK}
#             response['Authorization'] = authorization
#             # response['Token-Type']      =   'Bearer'
#             response['status'] = status.HTTP_200_OK
#         else:
#             header_response = {}
#             response['error'] = {'error': {
#                 'detail': 'Invalid credentials', 'status': status.HTTP_401_UNAUTHORIZED}}

#             return Response(response['error'], headers=header_response, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(response_result, headers=response, status=status.HTTP_200_OK)

# ?-----------------   TOKEN   LOG-IN -----------------------------------------------------------------------------------


# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         serializer = self.serializer_class(
#             data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         if user:
#             custom_user = CustomUser.objects.get(Q(user_id=user.pk))
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 'token': token.key,
#                 'user_id': user.pk,
#                 'username': user.username,
#                 'message': 'Login Successful'
#             })

#         else:
#             return Response({'message': "Something Went Wrong"})


# class ForgotPassword(APIView):

#     def post(self, request):

#         data = request.data
#         response = {}
#         response_result = {}
#         response_login = {}

#         email = data.get('email')
#         user_check = User.objects.get(email=email)
#         if user_check:

#             user_data = User.objects.get(email=email)
#             custom_user = CustomUser.objects.get(user_id=user_data.id)
#             message = 'Hello!\nIf you\'ve lost your Password or Wish to Reset it, use the below\n\n reset_id=' + \
#                 str(user_data.id)+'\n\n If you did not request a password reset, you can safely ignore this email. Only a person with access to your email can reset your account password.\n\nThanks\nAdmin'
#             subject = 'Reset Password - Robas '

#             email = EmailMessage(subject, message, to=[email])
#             email.send()
#             auth_token = jwt.encode(
#                 {'user_id': user_check.id, 'username': user_check.username, 'email': user_check.email, 'phone_number': custom_user.phone_number}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

#             serializer = CustomUserSerializer(user_check)

#             authorization = 'Bearer'+' '+auth_token
#             response_result['result'] = {
#                 'detail': 'link send in your email-id successfully', 'status': status.HTTP_200_OK}
#             response_login['Authorization'] = authorization
#             response_login['status'] = status.HTTP_200_OK

#         else:
#             header_response = {}
#             response_login['error'] = {'error': {
#                 'detail': 'Invalid credentials', 'status': status.HTTP_401_UNAUTHORIZED}}
#             header_response['status'] = status.HTTP_401_UNAUTHORIZED
#             header_response['detail'] = 'Invalid credentials'

#             return Response(response_login['error'], headers=header_response)

#         return Response(response_result, headers=response_login)


# class ForgotPasswordUpdate(APIView):

#     def post(self, request):

#         data = request.data
#         response = {}
#         response_result = {}
#         response_login = {}

#         id = data.get('reset_id')
#         password = data.get('new_password')
#         confirm_password = data.get('confirm_password')

#         user_check = User.objects.get(id=id)
#         if password == confirm_password:
#             if user_check:

#                 user_data = User.objects.get(id=id)
#                 custom_user = CustomUser.objects.get(user_id=user_data.id)

#                 user_data.set_password(password)
#                 user_data.save()

#                 message = 'Hello!\nYour password has been updated sucessfully. '
#                 subject = 'Password Updated Sucessfully '

#                 email = EmailMessage(subject, message, to=[user_data.email])
#                 email.send()
#                 auth_token = jwt.encode(
#                     {'user_id': user_check.id, 'username': user_check.username, 'email': user_check.email, 'phone_number': custom_user.phone_number}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

#                 serializer = CustomUserSerializer(user_check)

#                 authorization = 'Bearer'+' '+auth_token
#                 response_result['result'] = {
#                     'detail': 'link send in your email-id successfully', 'status': status.HTTP_200_OK}
#                 response_login['Authorization'] = authorization
#                 response_login['status'] = status.HTTP_200_OK
#                 return Response("Password Updated Sucessfully")
#             else:
#                 header_response = {}
#                 response_login['error'] = {'error': {
#                     'detail': 'Invalid credentials', 'status': status.HTTP_401_UNAUTHORIZED}}
#                 header_response['status'] = status.HTTP_401_UNAUTHORIZED
#                 header_response['detail'] = 'Invalid credentials'

#                 return Response(response_login['error'], headers=header_response)

#         else:
#             return Response("Password did not matched")

#         return Response(response_result, headers=response_login)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class CompanyModelViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# class CustomUserModelViewset(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomSerializer


#######################################################################
class CompanyApiView(GenericAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    def get(self, request):
        all_values = Company.objects.all().values()
        return Response({'result': all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        website = data.get('website')
        create_timestamp = data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')

        if Company.objects.filter(name=name).exists():
            return Response({'error': 'Name already exists'})

        else:

            all_values = Company.objects.create(
                name=name, website=website, create_timestamp=create_timestamp, last_update_timestamp=last_update_timestamp)
            return Response({'result': 'company created successfully'})


# class CustomapiView(GenericAPIView):
#     serializer_class = CustomSerializer
#     queryset = CustomUser.objects.all()


class ProjectExcelExport(APIView):

    def get(self, request):

        project_id = request.query_params.get('project_id')
        project_type = request.query_params.get('type')

        all_values = Project.objects.filter(Q(id=project_id) & Q(project_type_id=project_type)).values('id', 'company', 'client',
                                                                                                       'project_type',
                                                                                                       'service',
                                                                                                       'start_time',
                                                                                                       'end_time',
                                                                                                       'currency_value',
                                                                                                       'currency_ref',
                                                                                                       'incentive_cost',
                                                                                                       'total_completes',
                                                                                                       'targeted_audience',
                                                                                                       'quotes_ref',
                                                                                                       'length_of_interview',
                                                                                                       'status')

        dist_data = {'id': [],
                     'company': [],
                     'client': [],
                     'project_type': [],
                     'service': [],
                     'start_time': [],
                     'end_time': [],
                     'currency_value': [],
                     'currency_ref': [],
                     'incentive_cost': [],
                     'total_completes': [],
                     'targeted_audience': [],
                     'quotes_ref': [],
                     'length_of_interview': [],
                     'status': []
                     }

        for i in all_values:

            dist_data['id'].append(i['id'])
            dist_data['company'].append(i['company'])
            dist_data['client'].append(i['client'])
            dist_data['project_type'].append(i['project_type'])
            dist_data['service'].append(i['service'])
            dist_data['start_time'].append(i['start_time'])
            dist_data['end_time'].append(i['end_time'])
            dist_data['currency_value'].append(i['currency_value'])
            dist_data['currency_ref'].append(i['currency_ref'])
            dist_data['incentive_cost'].append(i['incentive_cost'])
            dist_data['total_completes'].append(i['total_completes'])
            dist_data['targeted_audience'].append(i['targeted_audience'])
            dist_data['quotes_ref'].append(i['quotes_ref'])
            dist_data['length_of_interview'].append(
                str(i['length_of_interview']))
            dist_data['status'].append(i['status'])

        # df = pd.DataFrame(dist_data)
        # current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M').replace(':', '-')
        # file_name = str(project_id) + str(project_type)+str(current_datetime)+'.xlsx'
        # writer = pd.ExcelWriter(path,
        #                 engine ='xlsxwriter')
        # df.to_excel(writer, sheet_name ='Sheet1', index= False)
        # writer.save()

        current_datetime = datetime.now().strftime(
            '%Y-%m-%d %H:%M').replace(':', '-').replace(' ', '_')
        file_name = str(project_id) + str(project_type) + \
            str(current_datetime)+'.xlsx'

        dff = pd.DataFrame(dist_data)
        path = settings.MEDIA_ROOT + '\\'+('test'+file_name)
        dff.to_excel(path, sheet_name='TEST SHEET', index=False)

        return Response({'file_url': 'http://127.0.0.1:8000/media/' + file_name})


class CustomApiView(GenericAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        all_values = CustomUser.objects.all().values('email')
        return Response(all_values)

    def post(self, request):
        data = request.data
        user = data.get('user')
        phone_number = data.get('phone_number')
        email = data.get('email')
        isAdmin = data.get('isAdmin')
        create_timestamp = data.get('create_timestamp')
        last_update_timestamp = data.get('last_update_timestamp')

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'})
        else:
            CustomUser.objects.create(user=user, phone_number=phone_number, email=email, isAdmin=isAdmin,
                                      create_timestamp=create_timestamp, last_update_timestamp=last_update_timestamp)
            return Response({'result': 'user created successfully'})

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  user registration  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

import uuid
from django.core.mail import send_mail

class UserRegister(APIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        if request.query_params:
            user_obj = UserAccess.objects.filter(user_id=request.query_params['id']).values('user_id', 'user__username','user__first_name','user__last_name','user__email','user__phone_number', 'access')
            return Response({'result': user_obj})
        else:
            value = CustomUser.objects.all().order_by('username').values('id', 'username', 'role__role_name', 'email', 'phone_number', )
            return Response({'result': {'users': value}})

    def post(self, request):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        isAdmin = data['isAdmin']

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error':"email already Taken"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': "username already Taken"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if isAdmin == False:
                random_password = "ROBAS"+str(uuid.uuid1())[:6]
                send_mail(
                    'Password',
                    'Your Instant Insight Username and Password Is \nlogin here '+settings.LIVE_URL+' \nusername:'+email+'\npassword:'+random_password,
                    'donotreplyrobas@gmail.com',
                    [email],
                    fail_silently=False,
                )

                user_obj = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                             email=email, phone_number=phone_number, isAdmin=False, password=make_password(random_password), company_id=data['comapny_id'], role_id=data['role_id'])            

                UserAccess.objects.create(user_id=user_obj.id, access=data['roles'])

                return Response({'result': {'registration': 'user registered successfully'}}, status=HTTP_200_OK)
            else:
                company_name = data['company']['name']
                company_website = data['company']['website']

                company = Company.objects.create(
                    name=company_name, website=company_website)
                
                user = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                                email=email, phone_number=phone_number, isAdmin=isAdmin, password=make_password(password), company_id=company.id)

                UserAccess.objects.create(user_id=user.id, access=[])

                auth_token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=12)}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                print(authorization)

                response = {}
                response['Authorization']=authorization
                return Response({'result': {'registration': 'user registered successfully'}}, headers=response, status=HTTP_200_OK)

    def put(self, request):
        data = request.data
        user_id = data['user_id']
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        isAdmin = data['isAdmin']

        if CustomUser.objects.filter(email=email).exists():
            if isAdmin == False:
                CustomUser.objects.filter(id=user_id).update(username=username, first_name=first_name, last_name=last_name,
                                             email=email, phone_number=phone_number, isAdmin=False, company_id=data['comapny_id'], role_id=data['role_id'])            

                UserAccess.objects.filter(user_id=user_id).update(access=data['roles'])
                return Response({'message': 'user updated successfully'})
            else:
                pass
            return Response({'message': {"user updated successfully"}})
        else:
            return Response({'message': 'user with this email does not exists'})

    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  User Login   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class UserLogin(generics.ListCreateAPIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = CustomUser.objects.filter(email=email)
        for user in user:
            username = user.username
            user_id = user.id
            company_id = user.company_id
            data = check_password(password, user.password)
        if user and data:
                print("========================",str(settings.JWT_SECRET_KEY))
                auth_token = jwt.encode({'user_id': user.id, 'name': user.username, 'exp': datetime.utcnow() + timedelta(days=5)}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = auth_token
                print(authorization)

                response = {}
                response['Authorization']=authorization

                userAccess = UserAccess.objects.get(user_id=user.id).access
                userAccessArr = []
                for ua in userAccess:
                    userAccessArr.append(ua['item_text'])


                return Response({'result': { 'user_info': {'username': username, 'user_id': user_id, 'company_id': company_id, 'token': response['Authorization']}, 'message': 'login successfull', 'access': userAccessArr}}, headers=response, status=HTTP_200_OK)
        return Response({'result': {'error': 'invalid credential'}}, status=status.HTTP_401_UNAUTHORIZED)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Add User @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2

class AddUsers(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):  
        value = CustomUser.objects.all().order_by('username').values()
        return Response({'Result': {'Users': value}})

    def post(self, request):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        company_id = data.get('company_id')

        role = data['role']
        isAdmin = False

        ps = string.ascii_letters+string.digits
        password = ''.join(random.sample(ps*8, 10))
        print(password)

        if CustomUser.objects.filter(username=username, email=email).exists():
            return Response({"username and email already Taken"}, status=HTTP_406_NOT_ACCEPTABLE)

        if role['id'] is not None:
            user = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name,
                                             email=email, phone_number=phone_number, isAdmin=isAdmin, company_id=company_id, role_id=role['id'])

                                
        else:
            role_name = role['role_name']
            permission = role['permission']

            role_data = RoleAccessControl.objects.create(
                role_name=role_name, permission=permission, company_id=company_id)

            print(role_data)

            user = CustomUser.objects.create(username=username, first_name=first_name, last_name=last_name, email=email,
                                             phone_number=phone_number, isAdmin=isAdmin,  password=make_password(password), company_id=company_id, role_id=role_data.id)

        return Response({'result': {'user': 'user added successfully'}})

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Forgot password @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


class changePassword(APIView):
    def post(self, request):
        print("request====",request)
        # fun =  CheckAuthData(request)
        print(fun.id)

        

        data = request.data
        old_password = data['old_password']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if new_password == confirm_password:
            pswrd = make_password(new_password)
            print(pswrd)

            CustomUser.objects.filter(id=fun.id).update(password = pswrd)
            return Response({'result': {'message': 'Password changed successfully'}})
        else:
            return Response({'result': {'message': 'password does not match'}}, status=HTTP_406_NOT_ACCEPTABLE)
        

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Forgot Password  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class forgotPassword(GenericAPIView):
    def post(self, request):
        data = request.data

        email = data['email']
        if CustomUser.objects.filter(email=email).exists():
            user_id = CustomUser.objects.get(email=email)
            print(user_id.id)
            full_name = user_id.first_name+" "+user_id.last_name
            
            # link = "https://robas.thestorywallcafe.com/#/reset-password/"+str(user_id.id)
            # link = "http://localhost:4200/reset-password/"+str(user_id.id)
            link = settings.LIVE_URL+'/reset-password/'+str(user_id.id)
            print(link)
            
            html_path = 'forgot_password.html'
            context_data = {'link': link, 'name': full_name}
            email_html_template = get_template(html_path).render(context_data)
            receiver_email = email
            email_msg = EmailMessage('Forgot Password??', email_html_template, settings.APPLICATION_EMAIL, [receiver_email], reply_to=[settings.APPLICATION_EMAIL])

            email_msg.content_subtype='html'
            email_msg.send(fail_silently=False)
            return Response({'result': {'message': 'we have sent you the mail, please check your mail'}})
        return Response({'error': {'message': 'email not found'}}, status=HTTP_404_NOT_FOUND)

# print(check_password("123","pbkdf2_sha256$260000$CRtWjgiSUZ1MFtW8vDYiId$/Eyi9eI5gR0rWTkyyonKaFPfCJ5NQXy5ZWvMv8e8GHY="))     

class resetPassword(GenericAPIView):
    def post(self, request):
        data = request.data

        reset_user_id = data['reset_user_id']
        password = data['password']
        confirm_password = data['confirm_password']

        if CustomUser.objects.filter(id=reset_user_id).exists():
            if password == confirm_password:
                CustomUser.objects.filter(id=reset_user_id).update(password=make_password(confirm_password))
                return Response({'result': {'message': 'password_updated successfully'}})
            else:
                return Response({'result': {'error': 'password does not match'}}, status=HTTP_404_NOT_FOUND)
        return Response({'result': {'error': 'invalid user id'}}, status=HTTP_404_NOT_FOUND)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@   Log-Out @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2

class LogoutApiView(GenericAPIView):
    def post(self, request):
        data = request.data

        user_id = data['user_id']
        
 

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, pk):
        if CustomUser.objects.filter(id=pk).exists():
            value =CustomUser.objects.filter(id=pk).values()
            return Response({'result': {'user': value}})
        return Response({'result': {'user': 'user not found'}}, status=HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        if CustomUser.objects.filter(id=pk).exists():
            CustomUser.objects.filter(id=pk).delete()
            return Response({'result': {'user': 'user deleted successfully'}})
        return Response({'result': {'user': 'user not found to delete'}}, status=HTTP_404_NOT_FOUND)
        

    def put(self, request, pk):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        company_id = data.get('company')
        isAdmin = data.get('isAdmin')
        creater_id = data.get('creater_id')
        role = data.get('role')
        
        if CustomUser.objects.filter(id=pk).exists():
            CustomUser.objects.filter(id=pk).update(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, isAdmin=isAdmin, company_id=company_id, role_id=role)
            return Response({'result': {'user': 'user updated successfully'}}) 
        return Response({'result': {'user': 'user not found to delete'}}, status=HTTP_404_NOT_FOUND)    
        


class RoleAccessControlView(APIView):
    def get(self, request):
        value = RoleAccessControl.objects.all().values()
        return Response({'Result': {'Role': value}})

    def post(self, request):
        data = request.data

        role_name = data['role_name']
        description = data['description']
        company = data['company']

        if Company.objects.filter(id=company).exists():
            role = RoleAccessControl.objects.create(role_name=role_name, company_id=company, description=description)
            return Response({'result': {'role': 'role created successfully'}})
        return Response({'result': {'role': 'company not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        RoleAccessControl.objects.filter(id=id).delete()
        return Response({'role Deleted'})
        


    




    


        
    

