import re
import os
import base64
from typing import Any
from datetime import date, datetime
from django.db.models.aggregates import Count
from django.db.models.expressions import Case
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from panelbuilding.models import *
from panelbuilding.serializers import *
from rest_framework import generics, status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from prescreener.models import *
from prescreener.serializers import *
from django.template.loader import get_template
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
import string
import random
from django.db.models import Q
from projects.models import *
from robas.task import sleepy, send_email_task
from comman.models import *
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule, IntervalSchedule
import requests
# import datetime
from django.utils import timezone
import time
import json
import secrets  
from projects.pagination import MyPagination
from account.models import Company
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import make_password, check_password


from surveyQuestionare.models import *
from django.core.exceptions import *
from itertools import groupby
from operator import itemgetter

import uuid
from rest_framework import viewsets
import itertools
from usersurvey.models import *
from robas.encrdecrp import encrypt
from sampling.models import *
from robas.encrdecrp import decrypt
from django.utils.decorators import method_decorator
from account.backends_ import *
import pandas as pd
import csv
from hashids import Hashids
from datetime import timedelta

# Create your views here.


class CampaignTypeView(ListAPIView):
    serializer_class = CampaignTypeSerializer
    queryset = CampaignType.objects.all()
    # pagination_class = MyPagination

    # def get(self, request):
    #     values = CampaignType.objects.all().values()
    #     return Response({'result': {'company_type': values}})

    def post(self, request):
        data = request.data
        name = data['name']
        if CampaignType.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
        CampaignType.objects.create(name=name)
        return Response({'result': {'campaign_type': 'campaign_type created successfully'}})

    def delete(self, request, pk):
        if CampaignType.objects.filter(id=pk).exists:
            CampaignType.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'campaign type deleted successfullt'}})
        return Response({'error': {'message': 'camapign type not found'}}, status=status.HTTP_404_NOT_FOUND)


class CommissionModelView(ListAPIView):
    serializer_class = CommissionModelSerializer
    queryset = CommissionModel.objects.all()
    # pagination_class = MyPagination
    
    # def get(self, request, *args, **kwargs):
    #     values = CommissionModel.objects.all().values()
    #     return Response({'result': {'commision_model': values}})

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        if CommissionModel.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
        CommissionModel.objects.create(name=name)
        return Response({'result': {'commission_model': 'commission_model created successfully'}})

    def delete(self, request, pk):
        if CommissionModel.objects.filter(id=pk).exists:
            CommissionModel.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'commission model deleted successfullt'}})
        return Response({'error': {'message': 'commission model id not found'}}, status=status.HTTP_404_NOT_FOUND)

import uuid
print(str(uuid.uuid1())[:5])

def convertBase64toPath(campaignImage, imgeName):
    split_base_url_data = campaignImage.split(';base64,')[1]
    imgdata1 = base64.b64decode(split_base_url_data)
    filename1 = "/"+settings.MAINDOMAIN_NAME+"/site/public/media/camapainImages/"+imgeName+'.png'
    camapainImages = '/camapainImages/'+imgeName+'.png'
    ss=  open(filename1, 'wb')
    print(ss)
    ss.write(imgdata1)
    ss.close()

    return camapainImages

class DeleteOrRestoreCampaign(APIView):
    def post(self, request):
        is_delete_or_restore_campaign = request.data['is_delete_or_restore_campaign']
        campaign_id = request.data['campaign_id']

        Campaign.objects.filter(id=campaign_id).update(is_deleted=is_delete_or_restore_campaign)


        today = datetime.datetime.today()
        after_90_days = today + timedelta(days=89)


        if is_delete_or_restore_campaign:
            clocked_obj = ClockedSchedule.objects.create(
                    clocked_time = after_90_days 
            )
            task_start = PeriodicTask.objects.create(name="DeleteCampaignAutoAfter90Days"+str(clocked_obj.id), task="panelbuilding.tasks.deleteCampaign",clocked_id=clocked_obj.id, one_off=True, kwargs=json.dumps({'campaign_id': campaign_id}))
        else:
            cloked_id = PeriodicTask.objects.get(kwargs=json.dumps({'campaign_id': campaign_id})).clocked_id
            ClockedSchedule.objects.filter(id=cloked_id).delete()

        return Response({'message': 'camapign is deleted updated successfully'})


class ExportOrCloneCampaign(APIView):
    def post(self, request):
        data = request.data

        if data['is_export']:
            response = HttpResponse(content_type='application/vnd.ms-excel')

            writer = csv.writer(response)

            writer.writerow(['Campaign Id', 'First name', 'Last name', 'Email', 'Status', 'DOB', 'Gender','Vendor Id', 'Date of Joining', 'City', 'State', 'Country', 'Age'])

            obj = UserSurvey.objects.filter(campaign_id=data['campaign_id']).values_list('campaign_id', 'first_name', 'last_name', 'email', 'status', 'dob', 'gender', 'supplier_id', 'date_of_joining','city', 'state', 'country', 'age')
            for i in obj:
                writer.writerow(i)
            response['Content-Disposition'] = 'attachment; filename="campaign.xls"'
            return response

        else:
            obj = Campaign.objects.get(id=data['campaign_id'])
            obj.id = None
            obj.campaign_name = obj.campaign_name + " Copy"
            obj.save()
            print("obj", obj.campaign_name)

            campaign_link = settings.LIVE_URL+"/c/cid="+str(obj.id)+"&sid=<#sid#>&tid={tid}"  # cid = campaign_id
            # survey_template_link = "https://robas.thestorywallcafe.com/surveyTemplate?cid="+str(campaign_obj.id) # cid = campaign_id
            survey_template_link = settings.LIVE_URL+"/campaign-login/cid="+str(obj.id)

            print("campaign Obj", obj.id)

            Campaign.objects.filter(id=obj.id).update(campaign_link=campaign_link, surveyTemplate_link=survey_template_link)

            return Response({'message': "camapaign cloned successfully"})

# @method_decorator([authorization_required], name='dispatch')
class CampaignView(viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    pagination_class = MyPagination
    queryset = Campaign.objects.filter(is_deleted=False).order_by('-id')

    def get_queryset(self):
        queryset = super().get_queryset()

        should_paginate = self.request.query_params.get('paginate', False)

        if should_paginate:
        
            page_size = self.request.query_params.get('page_size')
            if page_size is not None:
                self.pagination_class.page_size = int(page_size)
            
            page_number = self.request.query_params.get('page')
            if page_number is not None:
                self.pagination_class.page = int(page_number)

            return self.paginate_queryset(queryset)
        
        return queryset

    def retrieve(self, request, *args, **kwargs):
        try:    
            campaign_obj = Campaign.objects.get(id=kwargs['pk'])
            serializer = CampaignSerializer(campaign_obj)

            return Response({'result': {'campaign': serializer.data}, "company_id": campaign_obj.company_id, "campaign_type_id": campaign_obj.campaign_type_id, "commision_model": campaign_obj.commision_model_id})
        except:
            return Response({"ERROR":"INVALID Campaign ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)


    def create(self, request):
        serializer = CampaignSerializer(data=request.data)

        if Campaign.objects.filter(campaign_name=request.data['campaign_name']).exists():
            return Response({'error': 'Campaign Name Already Exists '}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if serializer.is_valid():
                campaign_obj = Campaign.objects.create(
                    market_type_id = request.data['market_type_id'],
                    campaign_name = request.data['campaign_name'],
                    lead_required = request.data['lead_required'],
                    start_date = request.data['start_date'],
                    length_of_interview = request.data['length_of_interview'],
                    is_quality_follow_up = request.data['is_quality_follow_up'],
                    description = request.data['description'],
                    is_relevantld_check = request.data['is_relevantld_check'],
                    cpa = request.data['cpa'],
                    end_data = request.data['end_data'],
                    recruitment_type = request.data['recruitment_type'],
                    token = request.data['token'],
                    company_id = request.data['company'],
                    campaign_type_id = request.data['campaign_type'],
                    commision_model_id = request.data['commision_model'],
                    live_survey_link_for_custom_panel_builidng = request.data['live_link'],
                    created_by_id = request.data['user_id'],
                    updated_by_id = request.data['user_id'],
                    p_created_date_time = datetime.datetime.now(),
                    status = "Draft"
                )

                if request.data['customised_campaign_template'] is not None:

                    campaign_image = convertBase64toPath(request.data['customised_campaign_template']['camapign_image'], request.data['campaign_name']+'sideImage')
                    campaign_logo = convertBase64toPath(request.data['customised_campaign_template']['camapign_logo'], request.data['campaign_name']+'logoImage')

                    Campaign.objects.filter(id=campaign_obj.id).update(
                        background_color = request.data['customised_campaign_template']['background_color'],
                        camapign_image = campaign_image,
                        camapign_logo = campaign_logo,
                        campaign_title = request.data['customised_campaign_template']['campaign_title'],
                        text_color = request.data['customised_campaign_template']['text_color'],
                    )
                

                pixcels = {}  

                campaign_object = Campaign.objects.get(id=campaign_obj.id)
                serializer_data = CampaignSerializer(campaign_object)

                campaign_link = settings.LIVE_URL+"/c/cid="+str(campaign_obj.id)+"&sid=<#sid#>&tid={tid}"  # cid = campaign_id
                # survey_template_link = "https://robas.thestorywallcafe.com/surveyTemplate?cid="+str(campaign_obj.id) # cid = campaign_id
                survey_template_link = settings.LIVE_URL+"/campaign-login/cid="+str(campaign_obj.id)

                print("campaign Obj", campaign_obj.id)

                Campaign.objects.filter(id=campaign_obj.id).update(campaign_link=campaign_link, surveyTemplate_link=survey_template_link)

                    

                Page.objects.create(name="Default", campaign_id=campaign_obj.id)
                Page.objects.create(name="Thank You", campaign_id=campaign_obj.id)
                Page.objects.create(name="Terminated", campaign_id=campaign_obj.id)

                if request.data['campaign_type'] == 2:
                    GeneratedPixcelCodeForCustomPanelBuilding.objects.create(
                        s2s_postback_pixel_code = settings.LIVE_URL+"/cid="+str(campaign_obj.id)+"&mid="+str(uuid.uuid1())[:5]+"&tid=<#tid#>", 
                        pixel_code_screen = "",
                        google_pixel_code = "",
                        facebook_pixel_code = "",
                        campaign_id = campaign_obj.id 
                    )

                    pixcels['iternal_pixcel'] = GeneratedPixcelCodeForCustomPanelBuilding.objects.filter(campaign_id = campaign_obj.id).values()
                    return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK", "data": serializer_data.data, 'postback_pixcel': pixcels['iternal_pixcel'] })  
                else:
                    print("")

                return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK", "data": serializer_data.data})  
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def update(self, request, *args, **kwargs):
        pixcels = {}

        if Campaign.objects.filter(~Q(id=kwargs['pk']) & Q(campaign_name=request.data['campaign_name'])).exists():
            return Response({'error': 'Campaign Name Already Exists '}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project_obj = Campaign.objects.get(id=kwargs['pk'])
            serializer = CampaignSerializer(project_obj, data=request.data, partial=True)
            if serializer.is_valid():
                # s_obj = serializer.save()
                Campaign.objects.filter(id=kwargs['pk']).update(
                market_type_id = request.data['market_type_id'],
                campaign_name = request.data['campaign_name'],
                lead_required = request.data['lead_required'],
                start_date = request.data['start_date'],
                length_of_interview = request.data['length_of_interview'],
                is_quality_follow_up = request.data['is_quality_follow_up'],
                description = request.data['description'],
                is_relevantld_check = request.data['is_relevantld_check'],
                cpa = request.data['cpa'],
                end_data = request.data['end_data'],
                recruitment_type = request.data['recruitment_type'],
                token = request.data['token'],
                company_id = request.data['company'],
                campaign_type_id = request.data['campaign_type'],
                commision_model_id = request.data['commision_model'],
                live_survey_link_for_custom_panel_builidng = request.data['live_link'],
                updated_by_id = request.data['user_id'],
                p_updated_date_time = datetime.datetime.now()
                )


                if request.data['customised_campaign_template'] is not None:
                    if ";base64," not in request.data['customised_campaign_template']['camapign_image'] or ";base64," not in request.data['customised_campaign_template']['camapign_logo']:
                        Campaign.objects.filter(id=kwargs['pk']).update(
                                background_color = request.data['customised_campaign_template']['background_color'],
                                campaign_title = request.data['customised_campaign_template']['campaign_title'],
                                text_color = request.data['customised_campaign_template']['text_color'],
                            )
                    else:
                        if os.path.isfile("/instantInsight/site/public/media/camapainImages/"+request.data['campaign_name']+'sideImage'+'.png'):
                            os.remove("/instantInsight/site/public/media/camapainImages/"+request.data['campaign_name']+'sideImage'+'.png')
                        if os.path.isfile("/instantInsight/site/public/media/camapainImages/"+request.data['campaign_name']+'logoImage'+'.png'):
                            os.remove("/instantInsight/site/public/media/camapainImages/"+request.data['campaign_name']+'logoImage'+'.png') 

                        campaign_image = convertBase64toPath(request.data['customised_campaign_template']['camapign_image'], request.data['campaign_name']+'sideImage')
                        campaign_logo = convertBase64toPath(request.data['customised_campaign_template']['camapign_logo'], request.data['campaign_name']+'logoImage')

                        print("updating")
                        Campaign.objects.filter(id=kwargs['pk']).update(
                            background_color = request.data['customised_campaign_template']['background_color'],
                            camapign_image = campaign_image,
                            camapign_logo = campaign_logo,
                            campaign_title = request.data['customised_campaign_template']['campaign_title'],
                            text_color = request.data['customised_campaign_template']['text_color'],
                        )
                

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Project.DoesNotExist as e:
            return Response({"ERROR":"INVALID CAMAPIGN ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)
        
        if request.data['campaign_type'] == 2:
            pixcels['iternal_pixcel'] = GeneratedPixcelCodeForCustomPanelBuilding.objects.filter(campaign_id = kwargs['pk']).values()
            return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK", "data": serializer.data, 'postback_pixcel': pixcels['iternal_pixcel'] })     
        else:
            return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK", "data": serializer.data})    

    def destroy(self, request, *args, **kwargs):
        try:
            camapaign_obj = self.get_object()
            camapaign_obj.delete()
            return Response({"result": {'project': 'campaign deleted successflly'}}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist as e:
            return Response({"ERROR":"INVALID CAMAPIGN ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)



class CamapignSupllierLink(APIView):
    def get(self, request):
        supplier_link_obj = SupplierCampaignLink.objects.filter(campaign_id=request.query_params['campaign_id'])
        serializer = SupplierCampaignLinkSerializer(supplier_link_obj, many=True)
        return Response({'result': serializer.data})
        
    def post(self, request):
        serializer = SupplierCampaignLinkSerializer(data=request.data)
        if serializer.is_valid():
            camapign_link = Campaign.objects.get(id=request.data['campaign'])

            if SupplierCampaignLink.objects.filter(Q(campaign_id=request.data['campaign']) & Q(supplier_id=request.data['supplier'])).exists():
                return Response({"MESSAGE": "CAMPAIGN IS ALREADY ASSIGNED FOR SELECTED SUPPLIER", "STATUS": "ERROR"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                supplier_obj = Supplier.objects.get(id=request.data['supplier'])
                supllier_camapign_link = camapign_link.campaign_link.replace('<#sid#>', str(request.data['supplier']))
                send_mail(
                    'New Offer',
                    'Congratulation You have Got The New Offer Start Sharing with Your\nCamapign Link\n'+supllier_camapign_link,
                    'gunjan@ekfrazo.in',
                    [supplier_obj.Email],
                    fail_silently=False,
                )

                supplier_link_obj = SupplierCampaignLink.objects.create(supplier_id = request.data['supplier'], campaign_id=request.data['campaign'], campaign_supplier_link=supllier_camapign_link)
            return Response({'RESULT': 'SUCCESSFULLY UPDATED CAMPAIGN LINK FOR THE SELECTED SUPPLIER', "STATUS": "SUCCESS"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request):
        if SupplierCampaignLink.objects.filter(id=request.query_params['id']).exists():
            supplier_link_obj = SupplierCampaignLink.objects.filter(id=request.query_params['id']).delete()
            return Response({'RESULT': 'DELETED', "STATUS": "SUCCESS"})
        return Response({'RESULT': 'NOT FOUND', "STATUS": "ERROR"})



class getCampaignDashBoard(APIView):
    def get(self, request, c_id):
        allVal = CampaignDashboard.objects.filter(campaign_id=c_id)
        campaign_name = CampaignDashboard.objects.filter(campaign_id=c_id).values('campaign__campaign_name')
        serializer = CampaignDashboardSerializer(allVal, many=True)
        return Response({'data': serializer.data, 'campaign_name': campaign_name})


# hashidss = Hashids(min_length=10)
# print("hashids = =>", hashidss)

# hashed_cid = hashidss.decode(str("shdh"))
# print("hashed_cid==>", hashed_cid)


from comman.getCountryDeatails import *


class CheckLink(APIView):
    def get(self, request):
        cid = request.query_params['cid']
        sid = request.query_params['sid']
        tid = request.query_params['tid']

        print("cid.isdigit()==>", cid.isdigit())

        if not cid.isdigit():
            return Response({'url':"invalid"})
        if not sid.isdigit():
            # return HttpResponse('{"Error": "Invalid"}') 
            return Response({'url':"invalid"})

        if Campaign.objects.filter(id=cid).exists():
            if Supplier.objects.filter(id=sid).exists():
            
                return Response({'url':"campaign?cid="+str(cid)+"&sid="+str(sid)+"&tid="+tid})

            # return HttpResponse('{"Error": "Invalid Supplier id"}')
            return Response({'url':"invalid"})
        # return HttpResponse('{"Error":"Invalid Campaign id"}')
        return Response({'url':"invalid"})


class CamapignLinkWithTransactionID(APIView):
    def get(self, request, cid, sid, tid):
        print("printing here line")

        ip_address = ""

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            ip_address = str(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            ip_address = str(ip)

        getCountryOfUser = getCountry(ip_address)
        print("getCountryOfUser==>>>***", getCountryOfUser)

        hashids = Hashids(min_length=8)

        hashed_cid = hashids.decode(str(cid))
        hashed_sid = hashids.decode(str(sid))

        print("hashed_cid==>", hashed_cid)

        # have to encrypt the camapaign is and suppier id

        # descrypted_cid = list(hashed_cid)[0]
        # descrypted_sid = list(hashed_sid)[0]

        # print("decryted sid and cid ==> ",descrypted_cid, descrypted_sid)
        
        # if type(sid)!= int and type(cid)!= int:
        #     return HttpResponse('{"Error":"Invalid"}')

        if not cid.isdigit():
            return HttpResponse('{"Error": "Invalid"}') 
        if not sid.isdigit():
            return HttpResponse('{"Error": "Invalid"}') 


        if Campaign.objects.filter(id=cid).exists():
            if Supplier.objects.filter(id=sid).exists():
                TransactionIds.objects.create(transaction_id=tid, supplier_id=sid, campaign_id=cid)

                total_clicks_count = TransactionIds.objects.filter(Q(campaign_id=cid) & Q(supplier_id=sid)).count()
                print("total_clicks_count ==>", total_clicks_count)
                # total_clicks_count = CampaignDashboard.objects.get(campaign_id=cid).total_clicks
                # print("total_clicks_count2==>>", total_clicks_count)
                # total_clicks_count = 0

                if UserSurvey.objects.filter(Q(campaign_id=cid) & Q(supplier_id=sid) & Q(status = "SOI")).exists():
                    soi = UserSurvey.objects.filter(Q(campaign_id=cid) & Q(supplier_id=sid) & Q(status = "SOI")).count()
                else:
                    soi = 0
                if UserSurvey.objects.filter(Q(campaign_id=cid) & Q(supplier_id=sid) & Q(status = "DOI")).exists():
                    doi = UserSurvey.objects.filter(Q(campaign_id=cid) & Q(supplier_id=sid) & Q(status = "DOI")).count()
                else:
                    doi = 0

                cpa = Campaign.objects.get(id=cid).cpa
                total_spent = (doi * int(cpa))

                # print("cpa=", cpa , "doi=", doi, "total_spent=", total_spent)

                conversion_rate = (doi + total_clicks_count) / 100

                if( CampaignDashboard.objects.filter(Q(campaign_id=cid) & Q( supplier_id=sid)).exists()):
                    CampaignDashboard.objects.filter(Q(campaign_id=cid) & Q( supplier_id=sid)).update(total_clicks = total_clicks_count, total_soi=soi, total_doi=doi, total_conversion_rate=conversion_rate, total_spent=total_spent, supplier_id=sid)
                else:
                    CampaignDashboard.objects.create(total_clicks = total_clicks_count, total_soi=soi, campaign_id=cid, supplier_id=sid, total_doi=doi, total_conversion_rate=conversion_rate, total_spent=total_spent)
                

                # print("all campaign==>",Campaign.objects.all().values())  

                if Campaign.objects.get(id=cid).live_survey_link_for_custom_panel_builidng is not None:
                    # print("Campaign.objects.get(id=cid).live_survey_link_for_custom_panel_builidng==>", Campaign.objects.get(id=cid).live_survey_link_for_custom_panel_builidng)
                    
                    return redirect(Campaign.objects.get(id=cid).live_survey_link_for_custom_panel_builidng)
                else:
                    return redirect(settings.LIVE_URL+"/campaign?cid="+str(cid)+"&sid="+str(sid)+"&tid="+tid)
                    # return redirect("https://instantinsightz.com/campaign?cid="+str(descrypted_cid)+"&sid="+str(descrypted_sid)+"&tid="+tid)
                    
            return HttpResponse('{"Error": "Invalid Supplier id"}')
        return HttpResponse('{"Error":"Invalid Campaign id"}')
       
class CampaignRoutingLogicQuestions(GenericAPIView):
    def get(self, request, pk, p_id):  #send campaign_id in id and page_id in pk

        res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=pk).values('question_library_id')
        q_id = []
        val = []
        questions = {}
        for i in res:
            qst = QuestionLibrary.objects.get(id=i['question_library_id'])
            q_id.append(qst.id)
            # print(qst.id ,"=",qst.question_text)
            questions['question_id'] = qst.id
            questions['question_text'] = qst.question_name
            val.append(questions)
            questions = {}

        val2 = []
        page = {}
        pg_id =[]

        all_pages_for_campaign = Page.objects.filter(campaign_id=p_id).values()
        for pges in all_pages_for_campaign:
            # print(pges['name'])
            if (pges['name'] == 'Thank You'):
                page['page_id'] = pges['id']
                page['page_name'] = pges['name']
                val2.append(page)
                page = {}
            if (pges['name'] == 'Terminated'):
                page['page_id'] = pges['id']
                page['page_name'] = pges['name']
                val2.append(page)
                page = {}

        exclude_page = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.exclude(page_id=pk).values() & PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=p_id).values()
        for j in exclude_page:
            pg_id.append(j['page_id'])

        # print(pg_id)
        pg_id2 = []
        for i in pg_id:
            if i not in pg_id2:
                pg_id2.append(i)
        
        for k in pg_id2:
            get_page = Page.objects.get(id=k)
            page['page_id']=get_page.id
            page['page_name']=get_page.name
            val2.append(page)
            page = {}

        print("targetpage ==>>", val2)
        return Response({'questions': val, 'targeted_page': val2}) 

class pixelCode(GenericAPIView):
    def get(self, request, cid):
        data = PixcelCode.objects.filter(campaign_id=cid).values()
        return Response({'data': data})

    def post(self, request):
        data = request.data

        pixel_code_screen = data['pixel_code_screen']
        s2s_postback_pixel_code = data['s2s_postback_pixel_code']
        google_pixel_code = data['google_pixel_code']
        facebook_pixel_code = data['facebook_pixel_code'] 
        campaign_id = data['campaign_id']

        if Campaign.objects.filter(id=campaign_id).exists():
            pixels = PixcelCode.objects.create(pixel_code_screen = pixel_code_screen, s2s_postback_pixel_code = s2s_postback_pixel_code, google_pixel_code = google_pixel_code, facebook_pixel_code = facebook_pixel_code, campaign_id=campaign_id)
            return Response({'result': {'message': 'pixelcode created successfully'}})
        return Response({'result': {'message': 'campaign not found'}}, status=HTTP_404_NOT_FOUND)

    def put(self, request):
        data = request.data

        pixel_code_screen = data['pixel_code_screen']
        s2s_postback_pixel_code = data['s2s_postback_pixel_code']
        google_pixel_code = data['google_pixel_code']
        facebook_pixel_code = data['facebook_pixel_code'] 
        campaign_id = data['campaign_id']

        if PixcelCode.objects.filter(campaign_id=campaign_id).exists():
            pixels = PixcelCode.objects.filter(campaign_id=campaign_id).update(pixel_code_screen = pixel_code_screen, s2s_postback_pixel_code = s2s_postback_pixel_code, google_pixel_code = google_pixel_code, facebook_pixel_code = facebook_pixel_code, campaign_id=campaign_id)
            return Response({'result': {'message': 'pixelcode updated successfully'}})
        return Response({'result': {'message': 'campaign not found'}}, status=HTTP_404_NOT_FOUND)


class CampaignStatus(GenericAPIView):
    def post(self, request):
        data = request.data

        campaign_id = data['campaign_id']
        status = data['status']

        if Campaign.objects.filter(id=campaign_id).exists():
            Campaign.objects.filter(id=campaign_id).update(status=status)
            return Response({'result': {'project is'+' '+status}})
        return Response({'error': {'message': 'campaign not found'}}, status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data
        status = data['status']
        if Campaign.objects.filter(id=pk).exists():
            Campaign.objects.filter(id=pk).update(status=status)
            return Response({'result': {'project is'+' '+status}})
        return Response({'error': {'message': 'campaign not found'}}, status=HTTP_404_NOT_FOUND)

class VendorView(ListAPIView):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()
    pagination_class = MyPagination

    # def get(self, request, *args, **kwargs):
    #     values = Vendor.objects.all().values()
    #     return Response({'Result': {'vendor': values}})

    def post(self, request):
        data = request.data

        name = data['name']
        market = data['market']
        cpa = data['cpa']
        cpi = data['cpi']
        cpc = data['cpc']
        cps = data['cps']
        cpl = data['cpl']
        compaign = data['compaign']

        if Campaign.objects.filter(id=compaign):
            Vendor.objects.create(name=name, market=market, cpa=cpa,
                                  cpi=cpi, cpc=cpc, cps=cps, cpl=cpl, compaign_id=compaign)
            return Response({'result': {'vendor': 'vendor created successfully'}})
        return Response({'result': {'error': 'no campaign found to create Vendor'}}, status=HTTP_404_NOT_FOUND)

class CamapignDateFilter(APIView):
    def post(self, request):
        data = request.data
        from_date = data['from_date']
        end_date = data['end_date']
        company = data['comapny']

        campaign_obj = Campaign.objects.filter(Q(start_date__gte=from_date) & Q(end_data__lte=end_date))
        serializer = CampaignSerializer(campaign_obj, many=True)
        return Response({'data':  serializer.data})

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk):
        if Vendor.objects.filter(id=pk).exists():
            val = Vendor.objects.filter(id=pk).values()
            return Response({'result': {'vendor': val}})
        return Response({'result': {'error': 'no vendor found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Vendor.objects.filter(id=pk).exists():
            Vendor.objects.filter(id=pk).delete()
            return Response({'result': {'vendor': 'vendor deleted successfully'}})
        return Response({'result': {'error': 'vendor not found'}}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data

        name = data['name']
        market = data['market']
        cpa = data['cpa']
        cpi = data['cpi']
        cpc = data['cpc']
        cps = data['cps']
        cpl = data['cpl']
        compaign = data['compaign']

        if Campaign.objects.filter(id=compaign).exists():
            if Vendor.objects.filter(id=pk).exists():
                Vendor.objects.filter(id=pk).update(
                    name=name, market=market, cpa=cpa, cpi=cpi, cpc=cpc, cps=cps, cpl=cpl, compaign_id=compaign)
                return Response({'result': {'vendor': 'vendor updated Successfully'}})
            return Response({'result': {'error': 'vendor not found'}}, status=HTTP_404_NOT_FOUND)
        return Response({'result': {'error': 'compaign not found'}}, status=HTTP_404_NOT_FOUND)

def verifyemailTemplate(request):
    return HttpResponseRedirect('hi')


class UserSurveyLogin(APIView):
    def post(self, request):
        data = request.data

        email = data['email']
        password = data['password']
        campaign_id = data['campaign_id']
        tid = data['tid']

        user_survey = UserSurvey.objects.get(email=email)

        data = check_password(password, user_survey.password)

        # iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')
        
        # encrypted_uid = encrypt(str(user_survey.id),iv)

        if user_survey and data==True :
            if campaign_id and tid is not None:
                campaign_obj = Campaign.objects.get(id=campaign_id)
                # url = "https://robas.thestorywallcafe.com/surveyTemplate?cid="+str(campaign_obj.id)+"&panelist_id="+str(user.id)+"&tid="+str(tid)
                url = "?cid="+str(campaign_obj.id)+"&panelist_id="+str(user_survey.id)+"&tid="+str(tid)
                return Response({'result': 'login sucess', "redirect_url": url, 'user_id': user_survey.id})
                # return redirect(url)
            else:
                url = ""
                return Response({'result': 'login sucess', 'user_id': user_survey.id, 'redirect_url': url})
        else:
            return Response({'result':'Please Check Credential'},  status=HTTP_406_NOT_ACCEPTABLE)

        # for user in user_survey:
        #     data = check_password(password, user.password)

        #     if user_survey.exists() and data==True:
        #         campaign_obj = Campaign.objects.get(id=campaign_id)
        #         # url = "https://robas.thestorywallcafe.com/surveyTemplate?cid="+str(campaign_obj.id)+"&panelist_id="+str(user.id)+"&tid="+str(tid)
        #         url = "?cid="+str(campaign_obj.id)+"&panelist_id="+str(user.id)+"&tid="+str(tid)
        #         return Response({'result': 'login sucess', "redirect_url": url})
        #         # return redirect(url)
        #     else:
        #         return Response({'result':'Please Check Credential'},  status=HTTP_406_NOT_ACCEPTABLE)
        


def supplierLinkredirect(updated_url):
    response = requests.get(url=updated_url)
    print("response ======",response.text, response.status_code)
    if (str(response.status_code) != "200"):
        return False
    else:
        return redirect(updated_url)

class CamapaignLoginRedirectView(APIView):
    def get(self, request, cid, sid, panelist_id, tid):
        url = PixcelCode.objects.get(campaign_id=cid).s2s_postback_pixel_code
        updated_url = url.replace("<#tid#>", tid)
        res = supplierLinkredirect(updated_url)
        if res == False:
            return HttpResponse("Invalid Transaction Id")
        else:
            print("res", res)
            UserSurvey.objects.filter(id=panelist_id).update(status="DOI")

            if VerifiedUserClicks.objects.filter(Q(panelist_id_id=panelist_id) & Q(campaign_id=cid) & Q(is_clicked=True)):
                pass
            else:
                VerifiedUserClicks.objects.create(panelist_id_id=panelist_id, campaign_id=cid, is_clicked=True)
                # UserSurveyPoints.objects.create(user_survey_id=panelist_id, points_earned=500)

            doi = UserSurvey.objects.filter(Q(status="DOI") & Q(campaign_id=cid) & Q(supplier_id=sid)).count()
            soi = UserSurvey.objects.filter(Q(status="SOI") & Q(campaign_id=cid) & Q(supplier_id=sid)).count()

            cpa = Campaign.objects.get(id=cid).cpa
            total_spent = (doi * int(cpa))

            CampaignDashboard.objects.filter(campaign_id=cid).update(total_doi=doi, total_soi=soi, total_spent=total_spent)
            # return redirect(settings.LIVE_URL+"/campaign-login?cid="+cid+"&panelist_id="+panelist_id+"&tid="+tid)
            return redirect(settings.LIVE_URL+"/email-verified?cid="+cid+"&panelist_id="+panelist_id+"&tid="+tid)


class CampaignSubmitApi(APIView):
    # serializer_class = UserSurveySerializer
    # queryset = UserSurvey.objects.all()
    # pagination_class = MyPagination

    def post(self, request):
        data = request.data

        campaign_id = data.get('campaign_id') #from formtend they has to stored from url and send id
        supplier_id = data.get('supplier_id')
        status= 'SOI'
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        gender = data.get('gender')
        DOB = data.get('DOB')
        tid = data.get('tid')
        password = data.get('password')
        city = data['city']
        state = data['state']
        country = data['country']
        # question_choice = data['question_choice'] 

        print("dob]===",DOB, datetime.datetime.strptime(DOB, '%d-%m-%Y'))
        

        # if UserSurvey.objects.filter(Q(email=email) & Q(campaign_id=campaign_id) & Q(supplier_id=supplier_id)).exists():
        if UserSurvey.objects.filter(email=email).exists():
            return Response({'ERROR': 'EMAIL ALREADY EXIST'}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            today = date.today()
            birthDate = datetime.datetime.strptime(DOB, '%d-%m-%Y')
            print("birthdate", birthDate)
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

            user_survey = UserSurvey.objects.create(first_name=first_name ,last_name=last_name ,email=email ,dob=DOB ,gender=gender, status=status, panelist_id=uuid.uuid4().int & (1<<30)-1, password=make_password(password), tid=tid, campaign_id=campaign_id, supplier_id=supplier_id, city=city, state=state, country=country, age=age)

            Answer.objects.create(user_survey_id=user_survey.id)

            soi_count = UserSurvey.objects.filter(Q(campaign_id=campaign_id) & Q(status = 'SOI')).count()

            if CampaignDashboard.objects.filter(Q(campaign_id=campaign_id) & Q(supplier_id=supplier_id)).exists():
                CampaignDashboard.objects.filter(Q(campaign_id=campaign_id) & Q(supplier_id=supplier_id)).update(campaign_id=campaign_id, total_soi=soi_count, supplier_id=supplier_id)
        
  
        camapaign_url = Campaign.objects.get(id=campaign_id).surveyTemplate_link
        url__ = camapaign_url+"&sid="+str(supplier_id)+"&panelist_id="+str(user_survey.id)+"&tid="+str(tid)

        url = PixcelCode.objects.get(campaign_id=campaign_id).s2s_postback_pixel_code
        updated_url = url.replace("<#tid#>", tid)

        print("url ===",updated_url)
        html_path = 'verify-email.html'
        context_data = {'name': first_name, 'email': email, 'url': url__}
        email_html_template = get_template(html_path).render(context_data)
        receiver_email = email
        email_msg = EmailMessage('Verify Email', email_html_template, settings.APPLICATION_EMAIL, [receiver_email],reply_to=[settings.APPLICATION_EMAIL])

        email_msg.content_subtype='html'
        email_msg.send(fail_silently=False)

        return Response({'result': {'campaign submit': 'campaign submitted successfully please check Your mail to verify email'}})
        

         #send otp to mobile


class CampaignVerify(APIView):
    # serializer_class = UserSurveySerializer
    # queryset = UserSurvey.objects.all()
    # pagination_class = MyPagination

    # def get(self, request):
    #     values = UserSurvey.objects.all().values()
    #     return Response({'Result': {'campain verify': values}})

    def post(self, request):
        data=request.data

        user_survey_id = data.get('user_survey_id')

        if UserSurvey.objects.filter(id=user_survey_id).exists():
            UserSurvey.objects.filter(id=user_survey_id).update(status="DOI", is_email_verified=True)
            UserSurveyPoints.objects.create(user_survey_id=user_survey_id ,points_spent=0, available_points=500, points_earned=500)
            # return redirect('')
            # return Response({'result': {'campaign verify': 'verified'}})
            return Response({'result': {'campaign verify':'campaign verified'}})


class Operators(generics.ListCreateAPIView):
    serializer_class = QuestionOperatorSerializer
    queryset = QuestionOperator.objects.all()
    pagination_class = MyPagination
    # def get(self, request):
    #     values = QuestionOperator.objects.all().values()
    #     return Response({'Result': {'Opeators': values}})

    def post(self, request):
        data = request.data
        name = data.get('name')
        company_id = data.get('company_id')

        if QuestionOperator.objects.filter(name=name).exists():
            return Response({'result': {'error': 'operator already exist'}}, status=HTTP_406_NOT_ACCEPTABLE)
        QuestionOperator.objects.create(name=name, company=company_id)
        return Response({'result': {'operator': {'operator created successfully'}}})

    # def delete(self, request, pk):
    #     if QuestionOperator.objects.filter(id=pk).exists:
    #         QuestionOperator.objects.filter(id=pk).delete()
    #         return Response({'result': {'message': 'operator deleted successfullt'}})
    #     return Response({'error': {'message': 'operator id not found'}}, status=status.HTTP_404_NOT_FOUND)

class SelectCriteria(APIView):
    def post(self, request):
        data = request.data

        question_id = data.get('question_id')
        operator_id = data.get('operator_id')
        answer = data.get('answer')
        format_type = data.get('format_type')

        # print("answer==>>", answer)

        if format_type is None:
            question_name = QuestionLibrary.objects.get(id=question_id)
            operator = QuestionOperator.objects.filter(id=operator_id).values()
            for i in operator:
                print(i['name'])
            # answers = Answer.objects.filter(answers=answer).values('answers')
            # answers = QuestionChoice.objects.filter(id__in=answer).values()
            # answerList = []
            # for k in answers:
            #     print(k['name'])
            #     answerList.append(k['name'])
            # for j in answer:
            data = Answer.objects.filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
            return Response({'result': {'count': data.count(),  'question_name': question_name.question_name, 'operator': i['name'], 'answers': "answerList"}})
        if format_type is not None:
            if format_type == 'agebetween':
                for i in answer:
                    count_by_date = Answer.objects.all().select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_date.values('user_survey_id').distinct().count(), 'data': count_by_date.values('user_survey__id').distinct()}})
            if format_type == 'date':
                for i in answer:
                    count_by_date = Answer.objects.all().select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_date.values('user_survey_id').distinct().count(), 'data': count_by_date.values('user_survey__id').distinct()}})
            if format_type == 'Age':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})
            if format_type == 'City':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})
            if format_type == 'Email':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})
            if format_type == 'Gender':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})
            if format_type == 'State':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})
            if format_type == 'Country':
                count_by_age = Answer.objects.select_related('user_survey').filter(Q_object_creater(self ,question_id, operator_id, answer, format_type))
                return Response({'result': {'count': count_by_age.values('user_survey_id').distinct().count(), 'data': count_by_age.values()}})

class BuildCriteria(APIView):
    def post(self, request):
        data = request.data  

        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer'], criterias[0]['format_type']))
        for i in range(1, len(criterias)):
            print(i)
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'], criterias[i]['format_type'])
            query.add(q_object, operator.get(criteria_operator[i-1]))

        # count_data = Answer.objects.filter(query).count()   
        count_data = Answer.objects.all().select_related('user_survey').filter(query)
                
        # print("count",count_data)
        
        data1 = Answer.objects.filter(query).values() 
        return Response({'result': {'count': count_data.values('user_survey_id').distinct().count(), 'requested_data': count_data.values('user_survey__email', 'user_survey__id', 'user_survey__country', 'user_survey__city').distinct() }})

class DrawSamples(GenericAPIView):
    def post(self, request):
        data = request.data
        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')
        format_type = data.get('format_type')
        drawsample = data['drawsample']
        quotas_detail = data['quotas_detail']
        project_id = data['project_id']

        emails = []

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer'], criterias[0]['format_type']))
        for i in range(1, len(criterias)):
            print(i)
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'], criterias[i]['format_type'])
            query.add(q_object, operator.get(criteria_operator[i-1]))

        # count_data = Answer.objects.filter(query).count() 
        count_data = Answer.objects.all().select_related('user_survey').filter(query).count()
        data1 = Answer.objects.all().select_related('user_survey').filter(query).values('user_survey__email', 'user_survey__campaign_id').distinct()

        # tempArr = []
        # tempDict = {}

        # tempSortedData = sorted(data1, key = itemgetter('user_survey__campaign_id'))
        # for key, value in groupby(data1, key = itemgetter('user_survey__campaign_id')):
        #     print("key==>",key)
        #     tempDict['campaign_id'] = key
        #     tempDict['emails'] = []
        #     for k in value:
        #         if k['user_survey__campaign_id'] == key:
        #             print("k value",k)
        #             tempDict['emails'].append(k['user_survey__email'])  
        #     tempArr.append(tempDict)
        #     tempDict = {}

        for d in data1:
            emails.append(d['user_survey__email'])
           
        secure_random = secrets.SystemRandom() 
        list_of_random_items = secure_random.sample(emails, drawsample)
        # print("random items",list_of_random_items)
        print(emails)

        Project.objects.filter(id=project_id).update(quotas_details=quotas_detail)

        return Response({'result': {'emails': list_of_random_items}})


class getAllPanelistEmail(APIView):
    def get(self, request):
        user_survey_obj = UserSurvey.objects.all().values('email')
        email_list = []
        for i in user_survey_obj:
            email_list.append(i['email'])
        return Response({'result': {'emails': email_list}})

ps = make_password("10259")
print(ps)
print(check_password("10259", ps))



class SendOut(APIView):
    def post(self, request):
        data = request.data 

        hashids = Hashids(min_length=8)

        template_id = data.get('template_id')
        shedule = data['shedule']
        emails = data['emails']
        project_id = data['project_id']
        custom_sample = data['custom_sample']
        
        val = EmailTemplate.objects.get(id=template_id)
        project_obj = Project.objects.get(id=project_id)
        sample_obj = Sampling.objects.filter(project_id=project_id).values('bonus_points').last()
        
        sender = val.sender
        subject = val.subject

        email_body = val.content

        soup = BeautifulSoup(email_body, 'html')
        clss = soup.find("a", class_="targetPage")

        clss_link_val = soup.find("a", class_="link_value")

        panelist_first_name = soup.find("span", class_="FirstName")
        panelist_last_name = soup.find("span", class_="LastName")
        surveyTime = soup.find("span", class_="Time")
        points = soup.find("span", class_="Points")

        print("==>> clas values", clss_link_val)

        if shedule is None:
            if custom_sample == True:
                for j in data['panelist_offer_links']:
                    clss_link_val.append(j['Offer link'])

                    encoded_user_id = hashids.encode(int(j['Panelist id']))

                    custom_offer_link = j['Offer link'].replace("<#id#>", str(encoded_user_id))
                    clss['href'] = custom_offer_link

                    print("class link==>", clss_link_val)

                    em_body = soup.prettify()
                    # send_email_task.delay(emails, sender, email_body, subject)                
                    email = EmailMessage(subject, em_body, from_email=sender, to=emails)
                    email.content_subtype = "html"
                    email.send(fail_silently=False)  

                    if UserSurveyOffers.objects.filter(Q(user_survey_id=j['Panelist id']) & Q(offer_link=custom_offer_link)).exists():
                        pass
                    else:
                        UserSurveyOffers.objects.create(user_survey_id=j['Panelist id'], offer_link=custom_offer_link, survey_name=project_obj.name, points_for_survey=sample_obj['bonus_points'], end_date=project_obj.end_date)
                return Response({'result': {'count': 'mail has been sent to all the panelist email ids'}})
            else:
                for i in emails:
                    panelist_obj = UserSurvey.objects.get(email=i)

                    panelist_first_name.string.replace_with(panelist_obj.first_name)
                    panelist_last_name.string.replace_with(panelist_obj.last_name)
                    surveyTime.string.replace_with(RequirementForm.objects.filter(project_id=project_id).last().actual_survey_length)
                    points.string.replace_with(Sampling.objects.filter(project_id=project_id).last().bonus_points)

                    panelist_id = panelist_obj.id
                    encoded_user_id = hashids.encode(int(panelist_id))

                    print("panelist id",panelist_id)
                    

                    # clss_link_val['href'] = RequirementForm.objects.get(project_id=project_id).masked_url_with_unique_id+"&uid="+str(encrypted_uid.decode("utf-8", "ignore"))

                    # clss['href'] = RequirementForm.objects.get(project_id=project_id).masked_url_with_unique_id+"&uid="+str(encoded_user_id)
                    # clss_link_val.append(RequirementForm.objects.get(project_id=project_id).masked_url_with_unique_id+"&uid=<#user_id#>")

                    clss['href'] = RequirementForm.objects.filter(project_id=project_id).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id)
                    clss_link_val.append(RequirementForm.objects.filter(project_id=project_id).last().masked_url_with_unique_id+"&uid=<#user_id#>")

                    em_body = soup.prettify()
                    # send_email_task.delay(emails, sender, email_body, subject)                
                    email = EmailMessage(subject, em_body, from_email=sender, to=[i])
                    email.content_subtype = "html"
                    email.send(fail_silently=False)  

                    if UserSurveyOffers.objects.filter(user_survey_id=panelist_id, offer_link=RequirementForm.objects.filter(project_id=project_id).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id)).exists():
                        pass
                    else:
                        UserSurveyOffers.objects.create(user_survey_id=panelist_id, offer_link=RequirementForm.objects.filter(project_id=project_id).last().masked_url_with_unique_id+"&uid="+str(encoded_user_id), survey_name=project_obj.name, points_for_survey=sample_obj['bonus_points'], end_date=project_obj.end_date)
                    

                    if ProjectDashboard.objects.filter(project_id=project_id, ie='internal').exists():
                        total_invite_sent = ProjectDashboard.objects.get(project_id=project_id, ie='internal').total_invite_sent
                        ProjectDashboard.objects.filter(project_id=project_id, ie='internal').update(total_invite_sent=int(total_invite_sent)+len(emails), total_clicks=0)
                    else:
                        ProjectDashboard.objects.create(project_id=project_id, total_invite_sent=len(emails), total_clicks=0, ie='internal')

            user_survey_obj = UserSurvey.objects.filter(email__in=emails).values()
            # print("list==>>",list(user_survey_obj))
            tempArr = []
            tempDict = {}

            tempSortedData = sorted(list(user_survey_obj), key = itemgetter('campaign_id'))
            for key, value in groupby(list(user_survey_obj), key = itemgetter('campaign_id')):
                if CampaignDashboard.objects.get(campaign_id=key).total_invite_sent:
                    tota_invite_sent = CampaignDashboard.objects.get(campaign_id=key).total_invite_sent
                else:
                    tota_invite_sent = 0

                print("total invite snet==>>", tota_invite_sent)

                print("key==>",key)
                tempDict['campaign_id'] = key
                tempDict['emails'] = []
                for k in value:
                    if k['campaign_id'] == key:
                        tempDict['emails'].append(k['email'])  
                        tempDict['email_count'] = len(tempDict['emails'])

                        print("==>>><<>>",type(tota_invite_sent), tota_invite_sent, tempDict['emails'])

                        updatedTotalInviteSentForEach_camapign = int(tota_invite_sent) + len(tempDict['emails'])

                        CampaignDashboard.objects.filter(campaign_id=k['campaign_id']).update(total_invite_sent=updatedTotalInviteSentForEach_camapign)
                tempArr.append(tempDict)
                tempDict = {}

            return Response({'result': {'count': 'mail has been sent to all the panelist email ids'}})


        # print(query)
        if shedule is not None:
            if custom_sample == True:
                for j in data['panelist_offer_links']:
                    clss_link_val.append(j['Offer link'])

                    encoded_user_id = hashids.encode(int(j['Panelist id']))

                    custom_offer_link = j['Offer link'].replace("<#id#>", str(encoded_user_id))
                    clss['href'] = custom_offer_link

                    print("class link==>", clss_link_val)

                    print("scheduled datetime==>", shedule['datetime']) 

                    clocked_obj = ClockedSchedule.objects.create(
                        clocked_time = shedule['datetime']
                    )

                    if UserSurveyOffers.objects.filter(Q(user_survey_id=j['Panelist id']) & Q(offer_link=custom_offer_link)).exists():
                        pass
                    else:
                        UserSurveyOffers.objects.create(user_survey_id=j['Panelist id'], offer_link=custom_offer_link, survey_name=project_obj.name, points_for_survey=sample_obj['bonus_points'], end_date=project_obj.end_date)
                return Response({'result': {'count': 'mail has been sent to all the panelist email ids'}})
            
            else:
                print("else scheduled datetime==>", shedule['datetime']) 

                clocked_obj = ClockedSchedule.objects.create(
                    clocked_time = shedule['datetime']
                )
                
                task_start = PeriodicTask.objects.create(name="schduleSendout"+str(clocked_obj.id), task="panelbuilding.tasks.ScheduleSendout",clocked_id=clocked_obj.id, one_off=True, kwargs=json.dumps({'emails': emails, 'sender': sender, 'email_body': email_body, 'subject': subject, 'project_id': project_id, 'project_name': project_obj.name, 'project_end_date': str(project_obj.end_date), 'bonus_points': sample_obj['bonus_points']}))

                return Response({'result': {'count': 'mail has been scheduled successfully'}})




class PanelistPrescreenerAnswer(APIView):
    def post(self, request):
        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        prescreener_id = data['prescreener_id']

        hashids = Hashids(min_length=8)
        ints = hashids.decode(str(panelist_id))
        # print("prscreener-==.eroror line==>>", ints,list(ints))
        if len(list(ints)) == 0:
            descrypted_uid = panelist_id
        else:
            descrypted_uid = list(ints)[0]
            # print(list(ints)[0])
        
        if PrescreenerSurvey.objects.filter(panelist_id=descrypted_uid).exists():
            # return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
            return Response("/already-attended-survey", status=HTTP_406_NOT_ACCEPTABLE)
        else:
            PrescreenerSurvey.objects.create(panelist_id=descrypted_uid, prescreener_id=prescreener_id)
            for i in answered_question:
                answers = str(i['option_id']).strip("[]")
                answe = answers.replace("'", " ")
                if len(list(ints)) == 0:
                    answer = ExternalSamplePanelistAnswer.objects.create(panelist_id=descrypted_uid, answers=answe, question_library_id=i['question_id'], prescreener_id=prescreener_id)
                else:
                    answer = Answer.objects.create(user_survey_id=descrypted_uid, answers=answe, question_library_id=i['question_id'], prescreener_id=prescreener_id)


                # for j in i['option_id']:
                #     data = PrescreenerSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j, prescreener_id=prescreener_id)
            return Response({'result': {'message': 'Thank you for your response', 'panelist_id': panelist_id}})

class PanelistCampaignAnswer(APIView):
    def post(self, request):
        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        campaign_id = data['campaign_id']
        
        if CampaignSurvey.objects.filter(panelist_id=panelist_id).exists():
            return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            data = CampaignSurvey.objects.create(panelist_id=panelist_id, campaign_id=campaign_id)
            for i in answered_question:
                print("i['option_id']==>>", i['option_id'])
                answers = str(i['option_id']).strip("[]")
                answe = answers.replace("'", " ")
                answer = Answer.objects.create(user_survey_id=panelist_id, answers=answe, question_library_id=i['question_id'])
                # for j in i['option_id']:
                #     data = CampaignSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j, campaign_id=campaign_id)
            return Response({'result': {'message': 'Thank you for your response', 'panelist_id': panelist_id}})

class PanelistPeCampaignAnswer(APIView):
    def post(self, request):

        print("printing pane engement link here")

        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        pecampaign_id = data['pecampaign_id']

        # iv =  '1234567891011121'.encode('utf-8')
        # byteuid = bytes(panelist_id, 'utf-8')

        # decrypted_uid = decrypt(byteuid.decode("utf-8", "ignore"),iv)

        # descrypted_uid = decrypted_uid.decode("utf-8", "ignore")

        # print("uid diff==>>",decrypted_uid, descrypted_uid)

        hashids = Hashids(min_length=8)
        ints = hashids.decode(str(panelist_id))
        descrypted_uid = list(ints)[0]
        print("printing in panel building module ===>>> ",list(ints)[0])

        pe_campaign_obj = PeCampaign.objects.get(id=pecampaign_id)
        
        if PeCampaignSurvey.objects.filter(panelist_id=descrypted_uid).exists():
            return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            PeCampaignSurvey.objects.create(panelist_id=descrypted_uid ,pecampaign_id=pecampaign_id)
            for i in answered_question:
                answers = str(i['option_id']).strip("[]")
                answe = answers.replace("'", " ")
                answer = Answer.objects.create(user_survey_id=descrypted_uid, answers=answe, question_library_id=i['question_id'])
                # for j in i['option_id']:
                    # data = PeCampaignSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j)

            print('session url=>', request.session['pe-campaign-offer-url'])

            UserSurveyOffers.objects.filter(offer_link = request.session['pe-campaign-offer-url']).update(is_attened=True)

            oldUserpoints = UserSurveyPoints.objects.get(user_survey_id=descrypted_uid).points_earned
            total_points = int(oldUserpoints) +  int(pe_campaign_obj.points)
            UserSurveyPoints.objects.filter(user_survey_id=descrypted_uid).update(points_earned=total_points)

            return Response({'result': {'message': 'Thank you for your response'}})

class EMailCommunique(APIView):
    def post(self, request):
        data = request.data 

        category = data.get('category')
        template_id = data.get('template_id')
        name = data.get('name')
        subject = data.get('subject')
        sender = data.get('sender')
        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')
        shedule = data['shedule']
        max_reminder_sent = data['max_reminder_sent']

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer']))
        for i in range(1, len(criterias)):
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'])
            query.add(q_object, operator.get(criteria_operator[i-1]))
        data = Answer.objects.filter(query).count()
        data1 = Answer.objects.filter(query).values()

        emails = []
        
        for d in data1:
            d1 = UserSurvey.objects.get(id=d['user_survey_id'])
            emails.append(d1.email)
        # print(emails)

        val = EmailTemplate.objects.get(id=template_id)
        
        email_body = val.content

        if shedule is None:
            send_email_task.delay(emails, sender, email_body, subject)

        # print(query)
        if shedule is not None:

            string = shedule['date']+" "+ shedule['time']
            date = datetime.datetime.strptime(string, "%d-%m-%Y  %H:%M:%S")

            # print (date)

            year = date.year
            month = date.month
            day = date.day
            hour = date.hour
            minute = date.minute
            second = date.second

            timezone.now()
            date_time = datetime.datetime(year, month, day, hour, minute, second)
            print(date_time)
            # schedule = ClockedSchedule.objects.create(clocked_time = date_time)
            # task = PeriodicTask.objects.create(clocked_id=schedule.id, one_off=True, name="sending_email_to_paelist4", task="robas.task.send_email_task", args=json.dumps([emails, sender, email_body, subject]))
            
            interval =  IntervalSchedule.objects.create(every=3, period='days')

            task = PeriodicTask.objects.create(start_time=date_time, name="sending_email_to_paelist4", task="robas.task.send_email_task", args=json.dumps([emails, sender, email_body, subject]), interval_id=interval.id)

            # print(schedule)
        return Response({'result': {'count': data}})

class PromotionalSendOut(APIView):
    def post(self, request):
        data = request.data 

        category = data.get('category')
        template_id = data.get('template_id')
        name = data.get('name')
        subject = data.get('subject')
        sender = data.get('sender')
        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')
        shedule = data['shedule']
        max_reminder_sent = data['max_reminder_sent']

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer']))
        for i in range(1, len(criterias)):
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'])
            query.add(q_object, operator.get(criteria_operator[i-1]))
        data = Answer.objects.filter(query).count()
        data1 = Answer.objects.filter(query).values()

        emails = []
        
        for d in data1:
            d1 = UserSurvey.objects.get(id=d['user_survey_id'])
            emails.append(d1.email)
        # print(emails)

        val = EmailTemplate.objects.get(id=template_id)
        
        email_body = val.content

        if shedule is None:
            send_email_task.delay(emails, sender, email_body, subject)

        # print(query)
        if shedule is not None:

            string = shedule['date']+" "+ shedule['time']
            date = datetime.datetime.strptime(string, "%d-%m-%Y  %H:%M:%S")

            # print (date)

            year = date.year
            month = date.month
            day = date.day
            hour = date.hour
            minute = date.minute
            second = date.second

            timezone.now()
            date_time = datetime.datetime(year, month, day, hour, minute, second)
            print(date_time)
            # schedule = ClockedSchedule.objects.create(clocked_time = date_time)
            # task = PeriodicTask.objects.create(clocked_id=schedule.id, one_off=True, name="sending_email_to_paelist4", task="robas.task.send_email_task", args=json.dumps([emails, sender, email_body, subject]))
            
            interval =  IntervalSchedule.objects.create(every=3, period='days')

            task = PeriodicTask.objects.create(start_time=date_time, name="sending_email_to_paelist4", task="robas.task.send_email_task", args=json.dumps([emails, sender, email_body, subject]), interval_id=interval.id)

            # print(schedule)
        return Response({'result': {'count': data}})


def Q_object_creater(self, question_id, operator_id, answer, format_type):
    # print("answer fun:",answer, format_type)
    if format_type is not None:
        # print("format type in function===>",format_type)
        if format_type == 'agebetween':
            print("asnser after if ==>>", answer)
            if len(answer) == 2:
                switcher = {
                    17 : Q(user_survey__age__range=[answer[0], answer[1]]), # between
                }
                return switcher.get(operator_id) 
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__date_of_joining=answer[0]), #is equal
                4 : ~Q(user_survey__date_of_joining=answer[0]), #is not equal
                5 : Q(user_survey__date_of_joining__in=answer[0]), #in list
                6 : ~Q(user_survey__date_of_joining__in=answer[0]), #not in list
                7 : (Q(user_survey__date_of_joining__in=answer) | Q(user_survey__date_of_joining__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__date_of_joining__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__date_of_joining__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__date_of_joining__gt=answer[0]), #is greater than
                14 : Q(user_survey__date_of_joining__lt=answer[0]), #is less than
                15 : Q(user_survey__date_of_joining__gt=answer[0]), # before 
                16 : Q(user_survey__date_of_joining__lt=answer[0]), # after  
            }
            return switcher.get(operator_id) 
        if format_type == 'date':
            print("asnser after if ==>>", answer)
            if len(answer) == 2:
                switcher = {
                    17 : Q(user_survey__date_of_joining__range=[answer[0], answer[1]]), # between
                }
                return switcher.get(operator_id) 
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__date_of_joining=answer[0]), #is equal
                4 : ~Q(user_survey__date_of_joining=answer[0]), #is not equal
                5 : Q(user_survey__date_of_joining__in=answer[0]), #in list
                6 : ~Q(user_survey__date_of_joining__in=answer[0]), #not in list
                7 : (Q(user_survey__date_of_joining__in=answer) | Q(user_survey__date_of_joining__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__date_of_joining__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__date_of_joining__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__date_of_joining__gt=answer[0]), #is greater than
                14 : Q(user_survey__date_of_joining__lt=answer[0]), #is less than
                15 : Q(user_survey__date_of_joining__gt=answer[0]), # before 
                16 : Q(user_survey__date_of_joining__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)  
        if format_type == "Age":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__age__exact=answer[0]), #is equal
                4 : ~Q(user_survey__age__exact=answer[0]), #is not equal
                5 : Q(user_survey__age__in=answer[0]), #in list
                6 : ~Q(user_survey__age__in=answer[0]), #not in list
                7 : (Q(user_survey__age__in=answer) | Q(user_survey__age__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__age__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__age__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__age__gt=answer[0]), #is greater than
                14 : Q(user_survey__age__lt=answer[0]), #is less than
                15 : Q(user_survey__age__gt=answer[0]), # before 
                16 : Q(user_survey__age__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)  
        if format_type == "City":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__city__exact=answer[0]), #is equal
                4 : ~Q(user_survey__city__exact=answer[0]), #is not equal
                5 : Q(user_survey__city__in=answer[0]), #in list
                6 : ~Q(user_survey__city__in=answer[0]), #not in list
                7 : (Q(user_survey__city__in=answer) | Q(user_survey__city__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__city__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__city__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__city__gt=answer[0]), #is greater than
                14 : Q(user_survey__city__lt=answer[0]), #is less than
                15 : Q(user_survey__city__gt=answer[0]), # before 
                16 : Q(user_survey__city__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)
        if format_type == "Email":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__email__exact=answer[0]), #is equal
                4 : ~Q(user_survey__email__exact=answer[0]), #is not equal
                5 : Q(user_survey__email__in=answer[0]), #in list
                6 : ~Q(user_survey__email__in=answer[0]), #not in list
                7 : (Q(user_survey__email__in=answer) | Q(user_survey__email__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__email__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__email__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__email__gt=answer[0]), #is greater than
                14 : Q(user_survey__email__lt=answer[0]), #is less than
                15 : Q(user_survey__email__gt=answer[0]), # before 
                16 : Q(user_survey__email__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)
        if format_type == "Gender":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__gender__exact=answer[0]), #is equal
                4 : ~Q(user_survey__gender__exact=answer[0]), #is not equal
                5 : Q(user_survey__gender__in=answer[0]), #in list
                6 : ~Q(user_survey__gender__in=answer[0]), #not in list
                7 : (Q(user_survey__gender__in=answer) | Q(user_survey__gender__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__gender__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__gender__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__gender__gt=answer[0]), #is greater than
                14 : Q(user_survey__gender__lt=answer[0]), #is less than
                15 : Q(user_survey__gender__gt=answer[0]), # before 
                16 : Q(user_survey__gender__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)
        if format_type == "State":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__state__exact=answer[0]), #is equal
                4 : ~Q(user_survey__state__exact=answer[0]), #is not equal
                5 : Q(user_survey__state__in=answer[0]), #in list
                6 : ~Q(user_survey__state__in=answer[0]), #not in list
                7 : (Q(user_survey__state__in=answer) | Q(user_survey__state__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__state__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__state__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__state__gt=answer[0]), #is greater than
                14 : Q(user_survey__state__lt=answer[0]), #is less than
                15 : Q(user_survey__state__gt=answer[0]), # before 
                16 : Q(user_survey__state__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)
        if format_type == "Country":
            switcher = {
                # 1 : Q(question_library_id=question_id),  #is fill
                # 2 : ~Q(question_library_id=question_id),  #is not filled
                3 : Q(user_survey__country__exact=answer[0]), #is equal
                4 : ~Q(user_survey__country__exact=answer[0]), #is not equal
                5 : Q(user_survey__country__in=answer[0]), #in list
                6 : ~Q(user_survey__country__in=answer[0]), #not in list
                7 : (Q(user_survey__country__in=answer) | Q(user_survey__country__icontains=answer)), #contains any of them
                8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                11 : Q(user_survey__country__gte=answer[0]), #is greater or equal to
                12 : Q(user_survey__country__lte=answer[0]), #is less tahn or equal to
                13 : Q(user_survey__country__gt=answer[0]), #is greater than
                14 : Q(user_survey__country__lt=answer[0]), #is less than
                15 : Q(user_survey__country__gt=answer[0]), # before 
                16 : Q(user_survey__country__lt=answer[0]), # after  
            }
            return switcher.get(operator_id)
    if format_type is None:
        switcher = {
                    1 : Q(question_library_id=question_id),  #is fill
                    2 : ~Q(question_library_id=question_id),  #is not filled
                    3 : Q(answers__iexact=answer) & Q(question_library_id=question_id), #is equal
                    4 : ~Q(answers__iexact=answer) & Q(question_library_id=question_id), #is not equal
                    5 : Q(answers__in=answer) & Q(question_library_id=question_id), #in list
                    6 : ~Q(answers__in=answer) & Q(question_library_id=question_id), #not in list
                    7 : (Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id)), #contains any of them
                    8 : ~Q(answers__in=answer) & Q(question_library_id=question_id) | Q(answers__icontains=answer) & Q(question_library_id=question_id), #Doest not contains any of them
                    9 : Q(answers__exact=answer) & Q(question_library_id=question_id), #contains all of them
                    10 : ~Q(answers__exact=answer) & Q(question_library_id=question_id), #Does not not contains all of them 
                    11 : Q(answers__gte=answer) & Q(question_library_id=question_id), #is greater or equal to
                    12 : Q(answers__lte=answer) & Q(question_library_id=question_id), #is less tahn or equal to
                    13 : Q(answers__gt=answer) & Q(question_library_id=question_id), #is greater than
                    14 : Q(answers__lt=answer) & Q(question_library_id=question_id), #is less than
                    15 : Q(answers__gt=answer) & Q(question_library_id=question_id), # before 
                    16 : Q(answers__lt=answer) & Q(question_library_id=question_id), # after
                }
        return switcher.get(operator_id)  






class GetLandingPageURL(GenericAPIView):
    def get(self, request):
        campaign_id= request.GET.get('campaign_id')
        Affsc_id= request.GET.get('Affsc_id')
        print('campaign_id=====', campaign_id)
        print('Affsc_id======', Affsc_id)

        ps = string.digits
        unique_t_id = "D-"+''.join(random.sample(ps*8, 8))+"-"+''.join(random.sample(ps*8, 10))
        print(unique_t_id)

        return Response({
            "Result": {
                "landiing page link": "https://robasresearch.o18.app/p?tid="+unique_t_id
            }
        })

class Reports(APIView):
    def post(self, request):
        data = request.data  

        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')
         
        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer']))
        for i in range(1, len(criterias)):
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'])
            query.add(q_object, operator.get(criteria_operator[i-1]))
        data = Answer.objects.filter(query).count()
        data1 = Answer.objects.filter(query).values()    
            
        res = {"question": "", "base": "", "percentage":[], "options": [{"title": "", "count": ""}]}
        over_all_count = {'over_all-count': data}
        
        data_set = []

        for i in criterias:
            for j in i['answer'].split(','):
                res['options'][0]['title']=j
                single_count = Answer.objects.filter(Q_object_creater(self ,i['question_id'], i['operator_id'], j)).count()
                res['options'][0]['count']=single_count

                quest = QuestionLibrary.objects.get(id=i['question_id'])
                res['question'] = quest.question_text

                base_count = Answer.objects.filter(question_library_id=i['question_id']).count()
                print(base_count)
                res['base'] = base_count

                data_set.append(res)
                # print(res)
                res = {"question": "", "base": "", "percentage":[], "options": [{"title": "", "count": ""}]}
        
        print(res)
        data_set.append(over_all_count)
        # print(query)
        return Response({'result': data_set})
        

class PanelistSummary(ListAPIView):
    def get(self, request):
        email = request.query_params.get('email')

        user_data = UserSurvey.objects.filter(email=email).values()

        return Response({'result': {'basic_details': user_data}})

#@@@@@@@@@@@@@@@@@@@@@@@ add question from Q-lib #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
class SelectQuestionLibrary(GenericAPIView):
    def post(self, request):
        data = request.data

        question_type = data['question_type']
        question_category = data['question_category']

        if QuestionLibrary.objects.filter(question_type_id=question_type).exists():
            if QuestionLibrary.objects.filter(question_category_id=question_category).exists():
                questions = QuestionLibrary.objects.filter(question_type_id=question_type, question_category_id=question_category).values('id', 'question_name', 'is_base_question')
                return Response({'result': {'questions': questions}})
            return Response({'error': {'message': 'question category not found'}}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': {'message': 'question type not found'}}, status=status.HTTP_404_NOT_FOUND)
        

#@@@@@@@@@@@@@@@@@  Build Creiteria @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class SelectQuestionForBuildCriteria(GenericAPIView):
    def post(self, request):
        data = request.data

        question_id = data['question_id']
        questions_type = data['questions_type']

        if QuestionLibrary.objects.filter(id=question_id).exists():
            qst = QuestionLibrary.objects.get(id=question_id)
            # print(qst.question_type_id)

            answrs = []
            all_choice = {}

            if questions_type == 'Plain Text':
                # print("plain text here==>>", questions_type)
                answer_obj = Answer.objects.filter(question_library_id=question_id).values()
                # print("answer_obj==>", list(answer_obj))
                for i in list(answer_obj):
                    all_choice['choice_id'] = i['answers']
                    all_choice['name'] = i['answers']
                    answrs.append(all_choice)
                    all_choice = {}

            qst_choice = QuestionChoice.objects.filter(question_library_id=question_id).values()
            # print(qst_choice)

            # answer_obj = Answer.objects.filter(question_library_id=question_id).values('question_library_id')
            # print("answer obj==>>>",answer_obj)

            # answrs = []
            # all_choice = {}
            for i in qst_choice:
                all_choice = {}
                # print(i)
                all_choice['choice_id'] = i['id']
                all_choice['name'] = i['name']

                answrs.append(all_choice)

            # print("answers==",answrs)

            question_type = QuestionType.objects.get(id=qst.question_type_id)
            # print(question_type.name)

            val = questionType(self ,question_type.name)
            # print(val)
                        
        
            return Response({'operators': val, 'answers': answrs})
        return Response({'eror':'question id not found'}, status=HTTP_404_NOT_FOUND)

def questionType(self, data):
    operatrs = QuestionOperator.objects.all()
    all_list = []
    all_operators = {}
    for i in operatrs:
        all_operators = {}
        all_operators['operator_id'] = i.id
        all_operators['name'] = i.name

        all_list.append(all_operators)

    operators = {
        'Single Select': [all_list[0], all_list[1], all_list[2], all_list[3], all_list[6], all_list[7]],
        'Multiple Select': [all_list[0], all_list[1], all_list[6], all_list[7]],
        'Check Box': [all_list[0], all_list[1], all_list[6], all_list[7]],
        'Multiple Choice': [all_list[0], all_list[1], all_list[4], all_list[5], all_list[6], all_list[7]],
        'Plain Text': [all_list[2], all_list[3], all_list[12], all_list[13], all_list[16]],
        'Radio Button': [all_list[0], all_list[1], all_list[4], all_list[5], all_list[2], all_list[3]],
        'Date': [all_list[2], all_list[3] ,all_list[10], all_list[11], all_list[14], all_list[15],  all_list[16]],
    }
    # print(data)
    return operators.get(data)

class CampaignPageApiView(GenericAPIView):
    def get(self, request): 
        campaign_id = request.query_params['campaign_id']

        # if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).exists():
        #     res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).values()
        #     # print(res)
        #     final_output = []


        #     page_id1 = []
        #     json_data = {'page_id': '','page_name': ''}
        #     for i in res:
        #         page_id1.append(i['page_id'])

        #     print("page_id1", page_id1) 
        #     page_id2 = list(dict.fromkeys(page_id1))
        #     print("page_id2", page_id2)   

        #     q_ids = []
        #     res2 = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id__in=page_id2).values('question_library_id')
        #     for j in res2:
        #         print(j)
        #         q_ids.append(j['question_library_id'])
        #     print("q_ids", q_ids)

        #     fpage = Page.objects.filter(id__in=page_id2).values()  
        #     for k in fpage:
        #         json_data['page_id'] = k['id']
        #         json_data['page_name'] = k['name']
        #         final_output.append(json_data)
        #         json_data = {}
        #     print("fpage", fpage)          
                    

        #     # print(final_output)
        #     return Response({'result': final_output})
        # return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)

        if Page.objects.filter(campaign_id=campaign_id).exists():
            final_output = Page.objects.filter(campaign_id=campaign_id).values()
            print(final_output)
            # final_output = []


            # page_id1 = []
            # json_data = {'page_id': '','page_name': ''}
            # for i in res:
            #     page_id1.append(i['page_id'])

            # print("page_id1", page_id1) 
            # page_id2 = list(dict.fromkeys(page_id1))
            # print("page_id2", page_id2)   

            # q_ids = []
            # res2 = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id__in=page_id2).values('question_library_id')
            # for j in res2:
            #     print(j)
            #     q_ids.append(j['question_library_id'])
            # print("q_ids", q_ids)

            # fpage = Page.objects.filter(id__in=page_id2).values()  
            # for k in fpage:
            #     json_data['page_id'] = k['id']
            #     json_data['page_name'] = k['name']
            #     final_output.append(json_data)
            #     json_data = {}
            # print("fpage", fpage)          
                        

            # print(final_output)
            return Response({'result': final_output})
        return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)


# class CampaignPageApiView(GenericAPIView):
#     def get(self, request): 
#         campaign_id = request.query_params['campaign_id']
#         print("quryparms===",campaign_id)

#         if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).exists():
#             res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).values()
#             # print(res)
#             final_output = []
#             page_id = []


#             json_data = {'page_id': '','page_name': '', 'questions':{'question_id': '','question_text': '', 'question_category': '', 'question_type': ''}}
#             for i in res:
#                 page_id.append(i['page_id'])
#                 questions = QuestionLibrary.objects.filter(id=i['question_library_id']).values()
#                 # print(questions)
#                 for k in questions:
#                     json_data['questions']['question_id']=k['id']
#                     json_data['questions']['question_text']=k['question_text']
#                     question_type = QuestionType.objects.get(id=k['question_type_id'])
#                     question_category = QuestionCategory.objects.get(id=k['question_category_id'])
#                     json_data['questions']['question_type']=question_type.name
#                     json_data['questions']['question_category']=question_category.name

#                 page = Page.objects.filter(id=i['page_id']).values()
#                 for j in page:
#                     json_data['page_id']=j['id']
#                     json_data['page_name']=j['name']
#                     final_output.append(json_data)
#                     json_data = {'page_id': '','page_name': '', 'questions':{'question_id': '','question_text': '', 'question_category': '', 'question_type': ''}}
                    

#             print(final_output)
#             return Response({'result': final_output})
#         return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)

class getLanguageForSurvey(APIView):
    def get(self, request):
        prescreener_id = request.GET.get('prescreener_id')
        campaign_id = request.GET.get('campaign_id')
        pe_campaign_id = request.GET.get('pe_campaign_id')
        survey_questionare_id = request.GET.get('survey_questionare_id')
        panelist_id = request.GET.get('panelist_id')


        language_available_for_camapign = []
        language_dict = {}

        if campaign_id:
            pcp_obj = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).values()
            for i in pcp_obj:
                # print(i['question_library'])
                lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=i['question_library_id']).values('created_question_language__language')
            return Response(lang_obj)

        if prescreener_id:  
            pcp_obj = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).values()
            for i in pcp_obj:
                # print(i['question_library'])
                lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=i['question_library_id']).values('created_question_language__language')
            return Response(lang_obj)

        if pe_campaign_id:  
            pcp_obj = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=pe_campaign_id).values()
            for i in pcp_obj:
                # print(i['question_library'])
                lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=i['question_library_id']).values('created_question_language__language')
            return Response(lang_obj)




class SurveyTemplateApiView(APIView):
    def get(self, request):
        prescreener_id = request.GET.get('prescreener_id')
        campaign_id = request.GET.get('campaign_id')
        pe_campaign_id = request.GET.get('pe_campaign_id')
        survey_questionare_id = request.GET.get('survey_questionare_id')
        panelist_id = request.GET.get('panelist_id')

        language = request.GET.get('language')

        print("language==>", language)
        

        print("panelistId===>>", panelist_id)

        if prescreener_id:
            pages_for_prescreener = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id, is_deleted_question=False).values()
        
            pages_ids = []
            for i in pages_for_prescreener:
                pages = Page.objects.filter(id=i['page_id'])
                for j in pages:
                    pages_ids.append(j.id)
            
            page_dict = {}
            page_list = []

            for k in list(set(pages_ids)):
                # print(k)
                page_Q = []
                page_questions = {}
                for p in PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=k,  is_deleted_question=False).values():
                    if(p['question_library_id']!= None):

                        if language !='english':
                            lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=p['question_library_id']).values()
                            page_dict["q_lib"] = []
                                # page_questions = {}

                            for langqst in lang_obj:
                                lngqs = QuestionLibrary.objects.filter(Q(id=langqst['created_question_language_id']) & Q(language=language)).values()
                                if list(lngqs) == []:
                                    pass
                                else:
                                    page_questions['question_id'] = list(lngqs)[0]['id']
                                    page_questions['question_name'] = list(lngqs)[0]['question_name']

                                    qs_type = QuestionType.objects.filter(id=list(lngqs)[0]['question_type_id']).values()
                                    for qs_ty in qs_type:
                                        page_questions.update({'question_type': qs_ty['name']})

                                    opt = QuestionChoice.objects.filter(question_library_id=list(lngqs)[0]['id']).values()
                                    print("opt==>>", opt)
                                        
                                    optionsList=[]
                                    options_data = {}
                                    for j in opt:
                                        options_data['opt_id'] = j['id']
                                        options_data['opt_text'] = j['name']
                                        optionsList.append(options_data)
                                        options_data = {}
                                        page_questions.update({'options': optionsList})

                                    page_Q.append(page_questions)
                                    page_questions = {}

                                page_dict["q_lib"] = page_Q

                            ###################################
                        else:

                            qs = QuestionLibrary.objects.get(id=p['question_library_id'])
                            # print(qs)
                            page_questions['question_id'] = qs.id
                            page_questions['question_name'] = qs.question_name

                            qs_type = QuestionType.objects.filter(id=qs.question_type_id).values()
                            for qs_ty in qs_type:
                                page_questions.update({'question_type': qs_ty['name']})

                            opt = QuestionChoice.objects.filter(question_library_id=p['question_library_id']).values()
                            
                            optionsList=[]
                            options_data = {}
                            for j in opt:
                                options_data['opt_id'] = j['id']
                                options_data['opt_text'] = j['name']
                                optionsList.append(options_data)
                                options_data = {}
                                page_questions.update({'options': optionsList})
                            
                            page_Q.append(page_questions)
                            page_questions = {}
                            
                            page_dict["q_lib"] = page_Q
                    else:
                        pass
                logics = PageRoutingLogic.objects.filter(page_id=k).values()
                logicsDict = {}
                routing_logics_list = []
                for log in logics:
                    routing_logics_list.append(log)
                    logicsDict.update({'routing_logic': routing_logics_list})

                piping = PagePipingLogic.objects.filter(page_id=k).values()
                piping_logics_list = []
                for pip in piping:
                    piping_logics_list.append(pip)
                    logicsDict.update({'piping_logic': piping_logics_list})          

                masking = PageMaskingLogic.objects.filter(page_id=k).values()
                masking_logics_list = []
                for mask in masking:
                    masking_logics_list.append(mask)
                    logicsDict.update({'masking_logic': masking_logics_list})

                page_object = Page.objects.get(id=k).name
                page_dict['page_id'] = k
                page_dict['page_name'] = page_object
                page_dict['logics'] = [logicsDict]
                page_list.append(page_dict)
                page_dict = {}

            sorted_data_by_page = sorted(page_list, key=lambda x: x["page_id"])
            return Response({'page_details': sorted_data_by_page})

        if campaign_id:
            # if UserSurvey.objects.fiter(panelist_id=panelist_id).exists():
            #     return Response({'error': {'message': 'Invalid User'}}, status=HTTP_406_NOT_ACCEPTABLE)
            if CampaignSurvey.objects.filter(Q(campaign_id=campaign_id) & Q(panelist_id=panelist_id)).exists():
                return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
            if UserSurvey.objects.filter(id=panelist_id).exists():
                pages_for_campaign = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).values()
        
                pages_ids = []
                for i in pages_for_campaign:
                    pages = Page.objects.filter(id=i['page_id'])
                    for j in pages:
                        pages_ids.append(j.id)
                
                page_dict = {}
                page_list = []

                for k in list(set(pages_ids)):
                    # print(k)
                    page_Q = []
                    page_questions = {}
                    for p in PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=k).values():
                        if(p['question_library_id']!= None):

                            ###################################
                            if language !='english':
                                lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=p['question_library_id']).values()
                                page_dict["q_lib"] = []
                                # page_questions = {}

                                for langqst in lang_obj:
                                    lngqs = QuestionLibrary.objects.filter(Q(id=langqst['created_question_language_id']) & Q(language=language)).values()
                                    if list(lngqs) == []:
                                        pass
                                    else:
                                        page_questions['question_id'] = list(lngqs)[0]['id']
                                        page_questions['question_name'] = list(lngqs)[0]['question_name']

                                        qs_type = QuestionType.objects.filter(id=list(lngqs)[0]['question_type_id']).values()
                                        for qs_ty in qs_type:
                                            page_questions.update({'question_type': qs_ty['name']})

                                        opt = QuestionChoice.objects.filter(question_library_id=list(lngqs)[0]['id']).values()
                                        print("opt==>>", opt)
                                        
                                        optionsList=[]
                                        options_data = {}
                                        for j in opt:
                                            options_data['opt_id'] = j['id']
                                            options_data['opt_text'] = j['name']
                                            optionsList.append(options_data)
                                            options_data = {}
                                            page_questions.update({'options': optionsList})

                                        page_Q.append(page_questions)
                                        page_questions = {}

                                    page_dict["q_lib"] = page_Q


                            ###################################
                            else:
                                qs = QuestionLibrary.objects.get(id=p['question_library_id'])
                                # print(qs)
                                page_questions['question_id'] = qs.id
                                page_questions['question_name'] = qs.question_name

                                qs_type = QuestionType.objects.filter(id=qs.question_type_id).values()
                                for qs_ty in qs_type:
                                    page_questions.update({'question_type': qs_ty['name']})

                                opt = QuestionChoice.objects.filter(question_library_id=p['question_library_id']).values()
                                
                                optionsList=[]
                                options_data = {}
                                for j in opt:
                                    options_data['opt_id'] = j['id']
                                    options_data['opt_text'] = j['name']
                                    optionsList.append(options_data)
                                    options_data = {}
                                    page_questions.update({'options': optionsList})
                                
                                page_Q.append(page_questions)
                                page_questions = {}
                                
                                page_dict["q_lib"] = page_Q
                        else:
                            pass
                    logics = PageRoutingLogic.objects.filter(page_id=k).values()
                    logicsDict = {}
                    routing_logics_list = []
                    for log in logics:
                        routing_logics_list.append(log)
                        logicsDict.update({'routing_logic': routing_logics_list})

                    piping = PagePipingLogic.objects.filter(page_id=k).values()
                    piping_logics_list = []
                    for pip in piping:
                        piping_logics_list.append(pip)
                        logicsDict.update({'piping_logic': piping_logics_list})          

                    masking = PageMaskingLogic.objects.filter(page_id=k).values()
                    masking_logics_list = []
                    for mask in masking:
                        masking_logics_list.append(mask)
                        logicsDict.update({'masking_logic': masking_logics_list})

                    page_object = Page.objects.get(id=k).name
                    page_dict['page_id'] = k
                    page_dict['page_name'] = page_object
                    page_dict['logics'] = [logicsDict]
                    page_list.append(page_dict)
                    page_dict = {}

                return Response({'page_details': page_list})
            else:
                return Response({'error': {'message': 'Invalid User'}}, status=HTTP_406_NOT_ACCEPTABLE)

        if pe_campaign_id:
            pages_for_campaign = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=pe_campaign_id).values()
        
            pages_ids = []
            for i in pages_for_campaign:
                pages = Page.objects.filter(id=i['page_id'])
                for j in pages:
                    pages_ids.append(j.id)
            
            page_dict = {}
            page_list = []

            for k in list(set(pages_ids)):
                # print(k)
                page_Q = []
                page_questions = {}
                for p in PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=k).values():
                    if(p['question_library_id']!= None):

                        ###################################
                        if language !='english':
                            lang_obj = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=p['question_library_id']).values()
                            page_dict["q_lib"] = []
                                # page_questions = {}

                            for langqst in lang_obj:
                                lngqs = QuestionLibrary.objects.filter(Q(id=langqst['created_question_language_id']) & Q(language=language)).values()
                                if list(lngqs) == []:
                                    pass
                                else:
                                    page_questions['question_id'] = list(lngqs)[0]['id']
                                    page_questions['question_name'] = list(lngqs)[0]['question_name']

                                    qs_type = QuestionType.objects.filter(id=list(lngqs)[0]['question_type_id']).values()
                                    for qs_ty in qs_type:
                                        page_questions.update({'question_type': qs_ty['name']})

                                    opt = QuestionChoice.objects.filter(question_library_id=list(lngqs)[0]['id']).values()
                                    print("opt==>>", opt)
                                        
                                    optionsList=[]
                                    options_data = {}
                                    for j in opt:
                                        options_data['opt_id'] = j['id']
                                        options_data['opt_text'] = j['name']
                                        optionsList.append(options_data)
                                        options_data = {}
                                        page_questions.update({'options': optionsList})

                                    page_Q.append(page_questions)
                                    page_questions = {}

                                page_dict["q_lib"] = page_Q


                            ###################################
                        else:

                            qs = QuestionLibrary.objects.get(id=p['question_library_id'])
                            # print(qs)
                            page_questions['question_id'] = qs.id
                            page_questions['question_name'] = qs.question_name

                            qs_type = QuestionType.objects.filter(id=qs.question_type_id).values()
                            for qs_ty in qs_type:
                                page_questions.update({'question_type': qs_ty['name']})

                            opt = QuestionChoice.objects.filter(question_library_id=p['question_library_id']).values()
                            
                            optionsList=[]
                            options_data = {}
                            for j in opt:
                                options_data['opt_id'] = j['id']
                                options_data['opt_text'] = j['name']
                                optionsList.append(options_data)
                                options_data = {}
                                page_questions.update({'options': optionsList})
                            
                            page_Q.append(page_questions)
                            page_questions = {}
                            
                            page_dict["q_lib"] = page_Q
                    else:
                        pass
                logics = PageRoutingLogic.objects.filter(page_id=k).values()
                logicsDict = {}
                routing_logics_list = []
                for log in logics:
                    routing_logics_list.append(log)
                    logicsDict.update({'routing_logic': routing_logics_list})

                piping = PagePipingLogic.objects.filter(page_id=k).values()
                piping_logics_list = []
                for pip in piping:
                    piping_logics_list.append(pip)
                    logicsDict.update({'piping_logic': piping_logics_list})          

                masking = PageMaskingLogic.objects.filter(page_id=k).values()
                masking_logics_list = []
                for mask in masking:
                    masking_logics_list.append(mask)
                    logicsDict.update({'masking_logic': masking_logics_list})

                page_object = Page.objects.get(id=k).name
                page_dict['page_id'] = k
                page_dict['page_name'] = page_object
                page_dict['logics'] = [logicsDict]
                page_list.append(page_dict)
                page_dict = {}

            return Response({'page_details': page_list})

        if survey_questionare_id:
            pages_for_survey = SurveyPanelQuestion.objects.filter(survey_id=survey_questionare_id).values()
       
            pages_ids = []
            for i in pages_for_survey:
                pages = SurveyPage.objects.filter(id=i['survey_page_id'])
                for j in pages:
                    pages_ids.append(j.id)
            
            page_dict = {}
            page_list = []

            for k in list(set(pages_ids)):
                page_Q = []
                page_questions = {}
                for p in SurveyPanelQuestion.objects.filter(survey_page_id=k).values():
                    if(p['question_id']!= None):
                        qs = Questions.objects.get(id=p['question_id'])
                        page_questions['question_id'] = qs.id
                        page_questions['question_name'] = qs.name

                        qs_type = Element.objects.filter(id=qs.element_id).values()
                        for qs_ty in qs_type:
                            page_questions.update({'element': qs_ty['name']})
                    
                        opt = QuestionOptions.objects.filter(question_id=p['question_id']).values()
                        
                        optionsList=[]
                        options_data = {}
                        for j in opt:
                            options_data['opt_id'] = j['id']
                            options_data['opt_text'] = j['name']
                            optionsList.append(options_data)
                            options_data = {}
                            page_questions.update({'options': optionsList})
                        
                        page_Q.append(page_questions)
                        page_questions = {}
                        
                        page_dict["q_lib"] = page_Q
                    else:
                        pass

                
                page_object = SurveyPage.objects.get(id=k)
                page_dict['page_id'] = k
                page_dict['page_name'] = page_object.name
                page_list.append(page_dict)
                page_dict = {}

            return Response({'page_details': page_list})


class PanlistDetailsAPI(APIView):
    def get(self, request, panelist_id):
        if UserSurvey.objects.filter(id=panelist_id).exists():
            data = UserSurvey.objects.filter(id=panelist_id).values()
            return Response({'result': data})
        return Response({'error': 'Not Found'})

    def put(self, request, panelist_id):
        data = request.data
        profileImage = data['profile_image']

        if UserSurvey.objects.filter(id=panelist_id).exists():

            if profileImage is not None:
                split_base_url_data = profileImage.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                filename1 = "/instantInsight/site/public/media/profileImage/"+data['first_name']+'.png'
                profile_image = '/profileImage/'+data['first_name']+'.png'
                ss=  open(filename1, 'wb')
                print(ss)
                ss.write(imgdata1)
                ss.close()

                UserSurvey.objects.filter(id=panelist_id).update(
                    first_name=data['first_name'],last_name=data['last_name'],gender=data['gender'],city=data['city'],state=data['state'],country=data['country'], dob=data['dob'], profile_image= profile_image
                )
            return Response({'message': 'user data updated successfully'})
        return Response({'error': 'Not Found'}, status=HTTP_404_NOT_FOUND)


class PanlistQuery(APIView):
    def get(self, request):
        if request.query_params:
            obj = UserQuery.objects.filter(panelist_id=request.query_params['panelist_id']).values()
            return Response({'result': obj})
        else:
            obj = UserQuery.objects.all().values('panelist_email', 'panelist_id').distinct()
            return Response({"result":obj})
            
    def post(self, request):
        data = request.data

        panelist_id = data['panelist_id']
        subject = data['subject']
        email_id = data['email_id']
        query = data['query']
        
        obj = UserQuery.objects.create(panelist_id=panelist_id, panelist_email=email_id, query=query, subject=subject) 

        return Response({'result': "success"})

    def put(self, request):
        data = request.data

        panelist_id = data['panelist_id']
        email_id = data['email_id']
        reply = data['reply']
        query_id = data['query_id']

        obj = UserQuery.objects.filter(Q(panelist_id=panelist_id) & Q(id=query_id)).update(reply_data=reply, is_solved=True) 

        return Response({'result': 'data updated'})

# from py'emailsx import get_data as xlsx_get
import xlrd

import numpy as np

class UploadCustomSample(APIView):
    def post(self, request):
        excel_file = request.FILES['excel_file']

        # data = xlsx_get(excel_file)

        # print(data)


        if not excel_file.name.endswith('.xlsx'):
            return Response({'Result': {'Error': 'File Format should be xlsx'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        dataframe = pd.read_excel(excel_file)

        lit_of_user_id = [int(item) for item in  dataframe['Panelist id'].tolist()]
        print("lit_of_user_id==>",lit_of_user_id)  

        dataframe.to_dict(orient='record')

        email_list = []
        for i in UserSurvey.objects.filter(id__in=lit_of_user_id).values('email'):
            email_list.append(i['email'])

        dict_obj = dataframe.to_dict(orient='record')
        for i in dict_obj:
            print(int(i['Panelist id']), i['Offer link'])
            # if UserSurveyOffers.objects.filter(Q(user_survey_id=int(i['Panelist id'])) & Q(offer_link=i['Offer link'])).exists():
            #     pass
            # UserSurveyOffers.objects.create(user_survey_id=int(i['Panelist id']), offer_link=i['Offer link'])

        
        return Response({'result': {'count': len(email_list), 'requested_data':email_list, 'dict_obj': dict_obj}})


