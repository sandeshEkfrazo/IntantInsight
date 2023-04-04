import itertools
from pydoc import cli
import re
import time
from django.shortcuts import redirect
from django.core import paginator
from django.core.checks.messages import Error
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from projects.models import *
from rest_framework import generics
from django.db.models import Q
from projects.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from projects.pagination import MyPagination
from robas.task import *
import datetime
from django.utils import timezone
import json
import time
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, PeriodicTask
from django.http.response import HttpResponse
import csv
import xlwt
from datetime import datetime
import string
import random
from django.core.paginator import Paginator
from masters.models import *
from account.models import Company
from sampling.models import Sampling
from prescreener.models import *
from comman.models import *
from usersurvey.models import *
from django.utils.decorators import method_decorator
from account.backends_ import *
from rest_framework import viewsets
from django.core.exceptions import *
import pandas as pd

# Create your views here.


class ExternalSamplingListApiView(ListAPIView):
    serializer_class = ExternalSamplingSerializer
    queryset = ExternalSampling.objects.all()
    pagination_class = MyPagination

@method_decorator([authorization_required], name='dispatch')
class EmailTemplateListApiView(ListAPIView):
    serializer_class = EmailTemplateSerializer
    queryset = EmailTemplate.objects.all()
    pagination_class = MyPagination

@method_decorator([authorization_required], name='dispatch')
class ProjectDateFilter(APIView):
    def post(self, request):
        data = request.data
        from_date = data['from_date']
        end_date = data['end_date']
        company = data['comapny']

        project_obj = Project.objects.filter(Q(start_date__gte=from_date) & Q(end_date__lte=end_date))
        serializer = ProjectSerializer(project_obj, many=True)
        return Response({'data':  serializer.data})

d = "Copy(1)"
print("d==>",d[5:-1], d.replace(d[5:-1] ,'2'))

@method_decorator([authorization_required], name='dispatch')
class ExportDuplicateIDsForProject(APIView):
    def post(self, request):
        data = request.data
        project_id = data['project_id']

        response = HttpResponse(content_type='application/vnd.ms-excel')

        writer = csv.writer(response)

        writer.writerow(['Project Id', 'Duplicate Panelist id', 'vendor_id', 'vendor_name', 'status'])

        # obj = IESamplingStatus.objects.select_related('project').select_related('user').all().values_list('project__id','project__name','project__status', 'user_id', 'user__email', 'user__city', 'user__date_of_joining', 'status')
        obj = DuplicateorFraudPanelistID.objects.filter(project_id=project_id).values_list('project_id','panelist_id', 'supplier_id', 'supplier_name', 'status')
        for i in obj:
            writer.writerow(i)
        response['Content-Disposition'] = 'attachment; filename="pecampaign.xls"'
        return response

@method_decorator([authorization_required], name='dispatch')
class ExportOrCopyProject(APIView):
    def post(self, request):
        data = request.data
        project_id = data['project_id']
        is_export = data['is_export']
        company_id = data['company_id']

        if is_export:
            response = HttpResponse(content_type='application/vnd.ms-excel')

            writer = csv.writer(response)

            writer.writerow(['Project Id', 'Panelist id', 'Start date', 'End date', 'Project Status', 'vendor','Client id', 'Market', 'Panelist Status', 'Start_time', 'End_time', 'OS', 'Browser', 'IP-address', 'Country', 'Vendor TID'])

            # obj = IESamplingStatus.objects.select_related('project').select_related('user').all().values_list('project__id','project__name','project__status', 'user_id', 'user__email', 'user__city', 'user__date_of_joining', 'status')
            obj = IESamplingStatus.objects.filter(project_id=project_id).values_list('project__id', 'user_id', 'project__start_date', 'project__end_date', 'project__status', 'supplier__Supplier_Name', 'client_id', 'project__market_type','status', 'survey_start_time', 'survey_end_time', 'os','browser', 'ip_adress', 'user_country', 'vendor_tid')
            for i in obj:
                writer.writerow(i)
            response['Content-Disposition'] = 'attachment; filename="pecampaign.xls"'
            return response
        else:
            obj = Project.objects.get(id=project_id)
            obj.id = None
            obj.name = obj.name + " Copy"
            # if obj.copy == obj.copy:
            #     count = int(obj.copy[5:-1])  + 1
            #     obj.copy = obj.copy.replace(obj.copy[5:-1], str(count))
            # else:
            #     obj.copy = "Copy(1)"
            obj.save()

            copied_project = Project.objects.last().id

            st = SurveyStatus.objects.filter(company=company_id)
            for st in st:
                redirect_link_prefix = "https://instantinsightz.com/survey-"+st.name+"?projects="+str(copied_project)
                data = redirect_link_prefix+"&status="+st.name+"&rid="+str(uuid.uuid1())[:16]+"&uid={uid}"
                data_create = ProjectRedirects.objects.create(link=data, project_id=copied_project, survey_status_id=st.id)
            return Response('copied successfully')


class DeleteOrRestoreProjectStatus(APIView):
    def post(self, request):
        is_deleted_or_restored_project = request.data['is_deleted_or_restored_project']
        project_id = request.data['project_id']

        Project.objects.filter(id=project_id).update(is_deleted=is_deleted_or_restored_project)

        return Response({'message': "Project Deleted successfully"})


@method_decorator([authorization_required], name='dispatch')
class ProjecttView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.query_params:
            status_obj = Project.objects.filter(status=self.request.query_params['status'])
            return status_obj
        else:
            CurrentDate = datetime.datetime.now()
            for i in Project.objects.all().values():


                internal_completed = IESamplingStatus.objects.filter(project_id=i['id'], IE='internal', status='completed').count()
                print("internal project==>"+ str(i['id']), str(internal_completed))


                external_sample_obj = ExternalSampling.objects.filter(project_id=i['id']).values('supplier_id', 'supplier__Supplier_Name')
                for j in external_sample_obj:
                    external_total_complete = IESamplingStatus.objects.filter(project_id=i['id'], IE='external', supplier_id=j['supplier_id'], status='completed').count()

                    print("external project==>"+ str(i['id']), str(external_total_complete))












                end_date_timestamp = i['end_date'].timestamp()
                end_date = datetime.datetime.fromtimestamp(end_date_timestamp)

                project_end_date = datetime.datetime.fromtimestamp(end_date_timestamp).strftime("%d/%m/%Y %H:%M")
                project_end_datetime = datetime.datetime.strptime(project_end_date, "%d/%m/%Y %H:%M")

                if CurrentDate > project_end_datetime:
                    print("closed project", i['id'])
                    Project.objects.filter(id=i['id']).update(status='Closed') 
                else:
                    print("draft project", i['id'])
                    Project.objects.filter(id=i['id']).update(status='Draft')

            allval = Project.objects.all()
            return allval

    def retrieve(self, request, *args, **kwargs):
        try:    
            project_obj = Project.objects.get(id=kwargs['pk'])
            serializer = ProjectSerializer(project_obj)

            dictSerializer = dict(serializer.data,)

            print("data and its type==>>", type(serializer), type(dictSerializer))
            if EnableRd.objects.filter(project_id=kwargs['pk']).exists():
                dictSerializer['enable_rd'] = EnableRd.objects.get(project_id=kwargs['pk']).enable_rd
                dictSerializer['risk'] = EnableRd.objects.get(project_id=kwargs['pk']).risk
            else:
                dictSerializer['enable_rd'] = False
                dictSerializer['risk'] = None
            
            serializer.data['client_id'] = project_obj.client_id
            # print("hasgdgsdgds",serializer.data)
            if RequirementForm.objects.filter(project_id=kwargs['pk']).exists():
                req_obj = RequirementForm.objects.filter(project_id=kwargs['pk'])
                for i in req_obj.values():
                    print(i)

                if Sampling.objects.filter(project=kwargs['pk']).exists():
                    sam_obj = Sampling.objects.filter(project=kwargs['pk'])
                    
                    if Prescreener.objects.filter(project = kwargs['pk']).exists():
                        prescreener_obj = Prescreener.objects.get(project = kwargs['pk'])
                    
                        return Response({'result': {'project_details': dictSerializer}, 'client_id': project_obj.client_id, 'prescreener_id': prescreener_obj.id, 'client_live_link':i['live_survey_link']})
                    else:
                        return Response({'result': {'project_details': dictSerializer}, 'client_id': project_obj.client_id, 'prescreener_id': None, 'client_live_link':i['live_survey_link']})
                else:
                    return Response({'result': {'project_details': dictSerializer}, 'client_id': project_obj.client_id,'prescreener_id': None,  'client_live_link':i['live_survey_link']})

        except Project.DoesNotExist as e:
                return Response({"ERROR":"INVALID PROJECT ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)

        return Response({'result': {'project_details': dictSerializer}, 'client_id': project_obj.client_id})
        
    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                project_obj = Project.objects.create(
                    name = request.data['name'],
                    incentive_cost = request.data['incentive_cost'],
                    cpi = request.data['cpi'],
                    total_complete = request.data['total_complete'],
                    remove_targeted_audience = request.data['remove_targeted_audience'],
                    bidding_manager = request.data['bidding_manager'],
                    study_type = request.data['study_type'],
                    length_of_interview = request.data['length_of_interview'],
                    market_type = request.data['market_type'],
                    country = request.data['country'],
                    bidding_id = request.data['bidding_id'],
                    device_compatibility = request.data['device_compatibility'],
                    enable_geo_location = request.data['enable_geo_location'],
                    requires_webcam = request.data['requires_webcam'],
                    estimated_incidence_rate_percentage = request.data['estimated_incidence_rate_percentage'],
                    project_manager = request.data['project_manager'],
                    company_id = request.data['company'],
                    client_id = request.data['client'],
                    project_type_id = request.data['project_type'],
                    service_id = request.data['service'],
                    currency_id = request.data['currency'],
                    # quotas_id = request.data['quotas'],
                    start_date = request.data['start_date'],
                    end_date = request.data['end_date'],
                    created_by_id = request.data['created_by'],
                    updated_by_id = request.data['updated_by'],
                )

                if request.data['enable_rd']:
                    EnableRd.objects.create(project_id=project_obj.id, enable_rd=request.data['enable_rd'], risk=request.data['risk'])

                total_spent = int(request.data['cpi']) * int(request.data['total_complete'])

                ProjectDashboard.objects.filter(project_id=project_obj.id).update(total_spent=total_spent)

                st = SurveyStatus.objects.filter(company=request.data['company'])
                for st in st:
                    redirect_link_prefix = "https://instantinsightz.com/survey-"+st.name+"?projects="+str(project_obj.id)
                    data = redirect_link_prefix+"&status="+st.name+"&rid="+str(uuid.uuid1())[:16]+"&uid={uid}"
                    data_create = ProjectRedirects.objects.create(link=data, project_id=project_obj.id, survey_status_id=st.id)  
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                
        except Exception as e:
            raise e          
        return Response({'result': {'id': project_obj.id, 'project_name': project_obj.name}, 'message': 'project created successfully'})

    def update(self, request, *args, **kwargs):
        try:
            project_obj = Project.objects.get(id=kwargs['pk'])
            serializer = ProjectSerializer(project_obj, data=request.data, partial=True)
            if serializer.is_valid():
                s_obj = serializer.save()

                if EnableRd.objects.filter(project_id=kwargs['pk']).exists():
                    EnableRd.objects.filter(project_id=kwargs['pk']).update(enable_rd=request.data['enable_rd'], risk=request.data['risk'])
                else:
                    EnableRd.objects.create(project_id=project_obj.id, enable_rd=request.data['enable_rd'], risk=request.data['risk'])
                
                total_spent = float(request.data['cpi']) * float(request.data['total_complete'])
                ProjectDashboard.objects.filter(project_id=kwargs['pk']).update(total_spent=total_spent)

                if Prescreener.objects.filter(project=project_obj.id).exists():
                    prescreener_obj = Prescreener.objects.get(project=project_obj.id)
                    return Response({'result': {'project_id': kwargs['pk'], 'project_name': project_obj.name, 'prescreener_id': prescreener_obj.id}, 'message': 'project updated successfuly'})      
                else:
                    return Response({'result': {'project_id': kwargs['pk'], 'project_name': project_obj.name, 'prescreener_id': None}, 'message': 'project updated successfuly'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Project.DoesNotExist as e:
            return Response({"ERROR":"INVALID PROJECT ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)
        return Response({'result': {'project_id': kwargs['pk'], 'project_name': project_obj.name, 'requirement_form_id': None, 'sampling_id': None, 'prescreener_id': None}, 'message': 'project updated successfuly'})

    def destroy(self, request, *args, **kwargs):
        try:
            project_obj = self.get_object()
            project_obj.delete()
            return Response({"result": {'project': 'project deleted successflly'}}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist as e:
            return Response({"ERROR":"INVALID PROJECT ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)


@method_decorator([authorization_required], name='dispatch')
class ProjectQuery(ListAPIView):
    def get(self, request):
        status = request.query_params.get('status')
        res = Project.objects.filter(status=status).values()

        projectData = []
        for i, j in itertools.zip_longest(res, range(len(res))):

            client = Client.objects.get(id=i['client_id'])
            market = Country.objects.get(id=i['country'])
            owner = Company.objects.get(id=int(i['company']))
            quotas = Quotas.objects.get(id=int(i['quotes_id']))

            res[j]['company_name'] = owner.name
            res[j]['client_name'] = client.clientname
            res[j]['market_name'] = market.name
            res[j]['quotas_name'] = quotas.name

            if RequirementForm.objects.filter(project_id=i['id']).exists():
                re_form = RequirementForm.objects.get(project_id=i['id'])
                res[j]['start_date'] = re_form.start_date
                res[j]['end_date'] = re_form.end_date
            else:
                res[j]['start_date'] = ""
                res[j]['end_date'] = ""

        return Response({'result': {'project': res}})

@method_decorator([authorization_required], name='dispatch')
class ProjectExport(APIView):
    def get(self, request, pk):
        project_id = Project.objects.get(id=pk)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=project.xlsx'

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet('projects')
        font_style = xlwt.XFStyle()
        row_num = 0
        font_style.font.bold = True

        columns = ['name', 'currency_value', 'incentive_cost', 'cpi', 'total_complate', 'remove_targeted_audience', 'user1', 'study_type', 'length_of_interview', 'status', 'market_type', 'market_list_of_country_id', 'bidding_id',
                   'device_compatibility', 'enable_geo_location', 'enable_ip_blocker', 'requires_webcam', 'collects_pii', 'estimated_incidence_rate_percentage', 'user2', 'company', 'client', 'project_type', 'service', 'currency', 'quotes']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Project.objects.filter(id=pk).values_list('name', 'currency_value', 'incentive_cost', 'cpi', 'total_complate', 'remove_targeted_audience', 'user1', 'study_type', 'length_of_interview', 'status', 'market_type', 'market_list_of_country_id',
                                                         'bidding_id', 'device_compatibility', 'enable_geo_location', 'enable_ip_blocker', 'requires_webcam', 'collects_pii', 'estimated_incidence_rate_percentage', 'user2', 'company', 'client', 'project_type', 'service', 'currency', 'quotes')

        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
        wb.save(response)
        return response

@method_decorator([authorization_required], name='dispatch')
class RedirectApi(GenericAPIView):
    def get(self, request, pk):
        data = request.data

        project_id = pk

        res = {"title": '', 'link': ''}
        data_set = []
        # if is_static_redirect == True:
        data = ProjectRedirects.objects.filter(project_id=pk).values()
        for i in data:
            s_s = SurveyStatus.objects.get(id=i['survey_status_id'])
            res['title'] = s_s.name
            res['link'] = i['link']
            data_set.append(res)
            res = {"title": '', 'link': ''}

        return Response({'result': {'links': data_set}})

    def put(self, request, pk):
        print(pk)
        data = request.data
        reuse_project_id = data['reuse_project_id']
        data = ProjectRedirects.objects.filter(
            project_id=reuse_project_id).values()

        for project in data:
            print(project['link'])
            ProjectRedirects.objects.filter(
                survey_status_id=project['survey_status_id'], project_id=pk).update(link=project['link'])

        return Response({'result': {'general link updated successfully'}}, status=HTTP_200_OK)

########################## Requirement-Form ###################################

@method_decorator([authorization_required], name='dispatch')
class RequirementFormList(ListAPIView):
    serializer_class = RequirementFormSerializer
    queryset = RequirementForm.objects.all()
    pagination_class = MyPagination

@method_decorator([authorization_required], name='dispatch')
class RequirementFormApi(GenericAPIView):
    def get(self, request, pk):
        try:
            val = RequirementForm.objects.filter(project_id=pk)
            serializer = RequirementFormSerializer(val, many=True)
        except:
            return Response({'result': {'message': 'no requirement form found'}})
        return Response({'result': {'requirement_form': serializer.data}})

    def post(self, request, pk):
        data = request.data

        survey_topic = data['survey_topic']
        
        subject_line = data['subject_line']
        actual_survey_length = data['actual_survey_length']
        target_audience_type = data['target_audience_type']
        b2b_b2c_dropdowns = data['b2b_b2c_dropdowns']
        target_audience_textbox = data['target_audience_textbox']
        de_dupe_needed = data['de_dupe_needed']
        live_survey_link = data['live_survey_link']
        test_survey_link = data['test_survey_link']
        de_dupe_project_id = data['de_dupe_project_id']
        # start_date = data['start_date']
        # end_date = data['end_date']

        # print(survey_topic)

        # x = time.localtime()

        # hour = str(x.tm_hour)
        # minute = str(x.tm_min)
        # seconds = str(x.tm_sec)

        # times = hour+":"+minute+":"+seconds

        # starting_date = start_date+" " + times
        # ending_date = end_date+" " + times

        # s_date = datetime.datetime.strptime(starting_date, "%d-%m-%Y  %H:%M:%S")
        # print(s_date)
        # e_date = datetime.datetime.strptime(ending_date, "%d-%m-%Y  %H:%M:%S")
        # print(e_date)



        #############   Please do not remove any commneted code from this application  ################ 



        # if Project.objects.filter(id=pk).exists():

        # if RequirementForm.objects.filter(project_id=pk).exists():
        #     return Response({'result': {'error': 'requirement form already exist with this project'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # else:
        if Project.objects.filter(id=pk).exists():
            requiremnet_create = RequirementForm.objects.create(survey_topic_id=survey_topic, subject_line=subject_line, actual_survey_length=actual_survey_length, target_audience_type=target_audience_type, b2b_b2c_dropdowns=b2b_b2c_dropdowns, target_audience_textbox=target_audience_textbox, de_dupe_needed=de_dupe_needed, live_survey_link=live_survey_link, test_survey_link=test_survey_link, project_id=pk, de_dupe_project_id=de_dupe_project_id)

            masked_url_for_client = "https://instantinsightz.com/pid="+str(pk)+"&mid="+str(uuid.NAMESPACE_X500.hex + uuid.uuid4().hex + uuid.uuid4().hex)

            RequirementForm.objects.filter(id=requiremnet_create.id).update(masked_url_with_unique_id=masked_url_for_client)


                ############  update status to active ################
            # shedule_start = ClockedSchedule.objects.create(
            #         clocked_time=s_date)
            # task_start = PeriodicTask.objects.create(name="updating_project_start"+str(pk), task="robas.task.project_task_active",clocked_id=shedule_start.id, one_off=True, args=json.dumps([pk]))

            # project_scheduler_start = ProjectScheduler.objects.create(
                    # project_id=pk, clock_id=shedule_start.id, task_id=shedule_start.id)

                    ############  update status to closed  ###############
            # shedule_end = ClockedSchedule.objects.create(clocked_time=e_date)
            # task_end = PeriodicTask.objects.create(name="updating_project_end"+str(requiremnet_create.id), task="robas.task.project_task_closed",
            #                                             clocked_id=shedule_end.id, one_off=True, args=json.dumps([pk]))
            # project_scheduler_end = ProjectScheduler.objects.create(project_id=pk, clock_id=shedule_end.id, task_id=task_end.id)

            return Response({'result': {'id': requiremnet_create.id, 'client_live_link': live_survey_link, "project_id": pk, 'reuirement_form': 'requirement_form created successfully'}})
        else:
            return Response({'result': 'project not found'})    


        #############   Please do not remove any commneted code from this application  ################ 

from robas.encrdecrp import decrypt
from hashids import Hashids
import time
import requests

class MaskedLinkClick(APIView):
    def get(self, request, pid, mid, uid):

        # to check the duplicate checks #
        # if EnableRd.objects.get(project_id=pid).enable_rd == True:
        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(uid))
        

        #     if r.json()['Respondent']['threat_potential_score'] >= 70:
        #         if DuplicateorFraudPanelistID.objects.filter(panelist_id=uid).exists():
        #             pass
        #         else:
        #             DuplicateorFraudPanelistID.objects.create(panelist_id=uid, project_id=pid, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])
        #         return HttpResponseRedirect("https://instantinsightz.com/survey-terminated")

        #     #------------------------------------#
        # else:

        #--------------------------------------------------------------#

        # if EnableRd.objects.get(project_id=pid).enable_rd == True:
        #     risk_level = EnableRd.objects.get(project_id=pid).risk

        #     risk_level_list = []
        #     for i in risk_level:
        #         print("risk level==>", i)
        #         risk_level_list.append(i['value'])

        #     if "low" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=29:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "medium" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=69:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "high" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=100:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "low" and "medium" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=69:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "low" and "high" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if (r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=29) or (r.json()['Respondent']['threat_potential_score'] >=70 and r.json()['Respondent']['threat_potential_score'] <=100):
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "medium" and "high" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=30 and r.json()['Respondent']['threat_potential_score'] <=100:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #     if "low" and "medium" and "high" in risk_level_list:
        #         r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #         if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=100:
        #             redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #             return HttpResponseRedirect(redirect_link)
        #         else:
        #             terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #             redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #             if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #                 pass
        #             else:
        #                 supplier_obj = Supplier.objects.get(id=sid)
        #                 DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #             return HttpResponseRedirect(redirect_terminate_link)

        #--------------------------------------------------------------#

        






        project_obj = Project.objects.get(id=pid)
        total_projects = IESamplingStatus.objects.filter(project_id=pid, status='completed').count()

        print("total_projects count==>", total_projects)

        if total_projects >= int(project_obj.total_complete):
            Project.objects.filter(id=pid).update(status="Closed")
        else:
            Project.objects.filter(id=pid).update(status="Draft")

        request.session['vid'] = False
        request.session['offer_url'] = "https://instantinsightz.com/pid="+str(pid)+"&mid="+str(mid)+"&uid="+str(uid)

        hashids = Hashids(min_length=8)
        ints = hashids.decode(str(uid))
        descrypted_uid = list(ints)[0]

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        if Prescreener.objects.filter(project=pid).exists():
            # generated_link = Prescreener.objects.get(project=pid).generated_link
            generated_link = Prescreener.objects.filter(project=pid).last().generated_link
            screening_link = generated_link.replace('<#id#>', str(uid))
            print("screening_link", screening_link, descrypted_uid)

            if PrescreenerSurvey.objects.filter(prescreener_id=Prescreener.objects.get(project=pid).id, panelist_id=int(descrypted_uid)).exists():
                return HttpResponseRedirect("https://instantInsightz.com/already-attended-survey") 
            return HttpResponseRedirect(screening_link)
        else:          
            # req = RequirementForm.objects.get(project_id=pid)
            req = RequirementForm.objects.filter(project_id=pid).last()
            live_link = str(req.live_survey_link)
            updated_link = live_link.replace('<#id#>', str(uid))

            if ProjectDashboard.objects.get(project_id=pid, ie='internal'):
                clicks = ProjectDashboard.objects.get(project_id=pid, ie='internal').total_clicks + 1
                ProjectDashboard.objects.filter(project_id=pid, ie='internal').update(total_clicks=clicks)
            else:
                ProjectDashboard.objects.create(project_id=pid,ie='internal', total_clicks=1)
            
            campaign_id = UserSurvey.objects.get(id=descrypted_uid).campaign_id
            if UserClicks.objects.filter(panelist_id_id=descrypted_uid, project_id=pid, campaign_id=campaign_id, is_clicked=True).exists():
                pass
            else:
                UserClicks.objects.create(panelist_id_id=descrypted_uid, project_id=pid, campaign_id=campaign_id, is_clicked=True)
                campaign_clicks = CampaignDashboard.objects.get(campaign_id=campaign_id).total_clicks + 1
                rr = campaign_clicks / CampaignDashboard.objects.get(campaign_id=campaign_id).total_invite_sent
                CampaignDashboard.objects.filter(campaign_id=campaign_id).update(total_clicks=campaign_clicks, total_response_rate=rr)
            
            project_obj = ProjectDashboard.objects.get(project_id=pid, ie='internal')
            response_rate = project_obj.total_clicks / project_obj.total_invite_sent
            ProjectDashboard.objects.filter(project_id=pid, ie='internal').update(response_rate=response_rate, ie='internal')

            
            print("pid==>", pid, int(descrypted_uid))
            if IESamplingStatus.objects.filter(project_id=pid, user_id=int(descrypted_uid), IE="internal").exists():
                obj = ProjectRedirects.objects.get(project_id=pid, survey_status_id=5).link
                live_link = str(obj)
                terminate_link = live_link.replace('{uid}', str(uid))
                print("already attened")
                return HttpResponseRedirect("https://instantInsightz.com/already-attended-survey")
            elif Project.objects.get(id=pid).total_complete == IESamplingStatus.objects.filter(project_id=pid, IE="internal").count():
                obj = ProjectRedirects.objects.get(project_id=pid, survey_status_id=2).link
                live_link = str(obj)
                quotas_full = live_link.replace('{uid}', str(uid))
                return HttpResponseRedirect(quotas_full)
                
            elif int(Project.objects.get(id=pid).total_complete) < IESamplingStatus.objects.filter(project_id=pid, IE="internal").count():
                obj = ProjectRedirects.objects.get(project_id=pid, survey_status_id=4).link
                live_link = str(obj)
                panel_duplicate = live_link.replace('{uid}', str(uid))
                return HttpResponseRedirect(panel_duplicate)
            else:
                request.session['start_time'] = current_time
                request.session['length_of_interview'] = Project.objects.get(id=pid).length_of_interview

                IESamplingStatus.objects.create(project_id=pid, user_id=int(descrypted_uid), IE="internal", survey_start_time=current_time)

                return HttpResponseRedirect(updated_link)
                # updated the count of started not completed here

def VendorMaskLinkSubFun(request, pid, sid, mid, vid):
    print("printing request alng with parameters", request, pid, sid, mid, vid)
    if ProjectDashboard.objects.filter(project_id=pid, ie='external', supplier_id_id=int(sid)).exists():
        pass
    else:
        ProjectDashboard.objects.create(project_id=pid, ie='external', complete = 0, quotas_full=0, terminated=0,quality_fail=0,panel_duplicate=0,supplier_id_id=int(sid))

    request.session['vid'] = True
    request.session['supplier_id'] = str(sid)
    if Prescreener.objects.filter(project=pid).exists():
        # generated_link = Prescreener.objects.get(project=pid).generated_link
        generated_link = Prescreener.objects.filter(project=pid).last().generated_link
        
        screening_link = generated_link.replace('<#id#>', str(vid))
        print("screening_link", screening_link)
        # return HttpResponseRedirect(screening_link)
        return screening_link
    else:
        # req = RequirementForm.objects.get(project_id=pid)
        req = RequirementForm.objects.filter(project_id=pid).last()
        live_link = str(req.live_survey_link)

        str(uuid.uuid1())[:11]

        print("str(vid)==>>", str(vid))

        request.session['client_transaction_id'] = str(vid)

        updated_link = live_link.replace('<#id#>', str(uuid.uuid1())[:11])
        print("updated_link", updated_link)

        if IESamplingStatus.objects.filter(Q(project_id=pid) & Q(user_id=vid)).exists():
            # return HttpResponseRedirect("https://instantinsightz.com/already-attended-survey")

            print("terminating")
            return "https://instantinsightz.com/already-attended-survey"
        else:
            print("going to live survey")
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            request.session['external_start_time'] = current_time

            
            # IESamplingStatus.objects.create(project_id=pid, IE="external", survey_start_time=current_time)
            return updated_link
            # return HttpResponseRedirect(updated_link)


a = ["a", "b", "c"]

if "a" and "b" in a:
    print("there")

class VendorMaskedLinkClick(APIView):
    def get(self, request, pid, sid, mid, vid):

        # VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        print("printig enable rd object==>>", EnableRd.objects.filter(project_id=pid).values())

        if EnableRd.objects.get(project_id=pid).enable_rd == True:
            risk_level = EnableRd.objects.get(project_id=pid).risk

            risk_level_list = []
            for i in risk_level:
                print("risk level==>", i)
                risk_level_list.append(i['value'])

            if "low" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=29:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "medium" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=69:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "high" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=100:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "low" and "medium" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=69:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "low" and "high" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if (r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=29) or (r.json()['Respondent']['threat_potential_score'] >=70 and r.json()['Respondent']['threat_potential_score'] <=100):
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "medium" and "high" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=30 and r.json()['Respondent']['threat_potential_score'] <=100:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

            if "low" and "medium" and "high" in risk_level_list:
                r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

                if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=100:
                    redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
                    return HttpResponseRedirect(redirect_link)
                else:
                    terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
                    redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

                    if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
                        pass
                    else:
                        supplier_obj = Supplier.objects.get(id=sid)
                        DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

                    return HttpResponseRedirect(redirect_terminate_link)

        if EnableRd.objects.get(project_id=pid).enable_rd == False:
            redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
            return HttpResponseRedirect(redirect_link)


        # if EnableRd.objects.get(project_id=pid).enable_rd == True and EnableRd.objects.get(project_id=pid).risk == 'low':

        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #     if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=29:
        #         redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #         return HttpResponseRedirect(redirect_link)
        #     else:
        #         terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #         redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #         if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #             pass
        #         else:
        #             supplier_obj = Supplier.objects.get(id=sid)
        #             DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #         return HttpResponseRedirect(redirect_terminate_link)

            
        # if EnableRd.objects.get(project_id=pid).enable_rd == True and EnableRd.objects.get(project_id=pid).risk == 'medium':

        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #     if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=69:
        #         redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #         return HttpResponseRedirect(redirect_link)
        #     else:
        #         terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #         redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #         if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #             pass
        #         else:
        #             supplier_obj = Supplier.objects.get(id=sid)
        #             DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #         return HttpResponseRedirect(redirect_terminate_link)

        # if EnableRd.objects.get(project_id=pid).enable_rd == True and EnableRd.objects.get(project_id=pid).risk == 'high':

        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #     if r.json()['Respondent']['threat_potential_score'] >=1 and r.json()['Respondent']['threat_potential_score'] <=100:
        #         redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #         return HttpResponseRedirect(redirect_link)
        #     else:
        #         terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #         redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #         if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #             pass
        #         else:
        #             supplier_obj = Supplier.objects.get(id=sid)
        #             DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #         return HttpResponseRedirect(redirect_terminate_link)


        # if EnableRd.objects.get(project_id=pid).enable_rd == False or EnableRd.objects.get(project_id=pid).enable_rd == None:
        #     redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        #     return HttpResponseRedirect(redirect_link)


        #######################----------------------######################

        # else:
        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))
            
        #     terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #     redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #     if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #         pass
        #     else:
        #         supplier_obj = Supplier.objects.get(id=sid)
        #         DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #     return HttpResponseRedirect(redirect_terminate_link)
                



        # to check the duplicate checks #
        # if EnableRd.objects.get(project_id=pid).enable_rd == True:

        #     r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(vid))

        #     print(r.json())

        #     if r.json()['Respondent']['threat_potential_score'] >= 70:
        #         terminated_link = ExternalSampling.objects.filter(project_id=pid, supplier_id=sid).values('terminated_link')
        #         redirect_terminate_link = list(terminated_link)[0]['terminated_link'].replace('<#id#>', str(vid))

        #         if DuplicateorFraudPanelistID.objects.filter(panelist_id=vid).exists():
        #             pass
        #         else:
        #             supplier_obj = Supplier.objects.get(id=sid)
        #             DuplicateorFraudPanelistID.objects.create(panelist_id=vid, project_id=pid, supplier_id=sid, supplier_name=supplier_obj.Supplier_Name, status='terminated', threat_potential= r.json()['Respondent']['threat_potential'] ,threat_potential_score= r.json()['Respondent']['threat_potential_score'], duplicate_score=r.json()['Surveys'][0]['duplicate_score'])

        #         return HttpResponseRedirect(redirect_terminate_link)

            #------------------------------------#
        # redirect_link = VendorMaskLinkSubFun(request, pid, sid, mid, vid)
        # return HttpResponseRedirect(redirect_link)

        # if ProjectDashboard.objects.filter(project_id=pid, ie='external', supplier_id_id=int(sid)).exists():
        #     pass
        # else:
        #     ProjectDashboard.objects.create(project_id=pid, ie='external', complete = 0, quotas_full=0, terminated=0,quality_fail=0,panel_duplicate=0,supplier_id_id=int(sid))

        # request.session['vid'] = True
        # request.session['supplier_id'] = str(sid)
        # if Prescreener.objects.filter(project=pid).exists():
        #     # generated_link = Prescreener.objects.get(project=pid).generated_link
        #     generated_link = Prescreener.objects.filter(project=pid).last().generated_link
            
        #     screening_link = generated_link.replace('<#id#>', str(vid))
        #     print("screening_link", screening_link)
        #     return HttpResponseRedirect(screening_link)
        # else:
        #     # req = RequirementForm.objects.get(project_id=pid)
        #     req = RequirementForm.objects.filter(project_id=pid).last()
        #     live_link = str(req.live_survey_link)

        #     str(uuid.uuid1())[:11]

        #     print("str(vid)==>>", str(vid))

        #     request.session['client_transaction_id'] = str(vid)

        #     updated_link = live_link.replace('<#id#>', str(uuid.uuid1())[:11])
        #     print("updated_link", updated_link)

        #     if IESamplingStatus.objects.filter(Q(project_id=pid) & Q(user_id=vid)).exists():
        #         return HttpResponseRedirect("https://instantinsightz.com/already-attended-survey")
        #     else:
        #         now = datetime.datetime.now()
        #         current_time = now.strftime("%H:%M:%S")
        #         request.session['external_start_time'] = current_time

        #         # IESamplingStatus.objects.create(project_id=pid, IE="external", survey_start_time=current_time)
        #         return HttpResponseRedirect(updated_link)
        
@method_decorator([authorization_required], name='dispatch')
class RequirementFormDetailApi(GenericAPIView):
    def get(self, request, pro, req):
        if RequirementForm.objects.filter(Q(id=req) & Q(project_id=pro)).exists():
            val = RequirementForm.objects.filter(id=req).values()
            return Response({"result": {'requirement_form': val}})
        return Response({'result': {'error': 'requirement form or project not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pro, req):
        if RequirementForm.objects.filter(Q(id=req) & Q(project_id=pro)).exists():
            val = RequirementForm.objects.filter(id=req).delete()
            return Response({"result": {'requirement_form': 'requirement form deleted successfully'}})
        return Response({'result': {'error': 'requirement form or project not found to delete'}}, status=HTTP_404_NOT_FOUND)

    def put(self, request, req, pro):
        data = request.data

        survey_topic = data['survey_topic']
        subject_line = data['subject_line']
        actual_survey_length = data['actual_survey_length']
        target_audience_type = data['target_audience_type']
        b2b_b2c_dropdowns = data['b2b_b2c_dropdowns']
        target_audience_textbox = data['target_audience_textbox']
        de_dupe_needed = data['de_dupe_needed']
        live_survey_link = data['live_survey_link']
        test_survey_link = data['test_survey_link']
        de_dupe_project_id = data['de_dupe_project_id']
        # start_date = data['start_date']
        # end_date = data['end_date']

        x = time.localtime()

        # hour = str(x.tm_hour)
        # minute = str(x.tm_min)
        # seconds = str(x.tm_sec)

        # times = hour+":"+minute+":"+seconds

        # starting_date = start_date+" " + times
        # ending_date = end_date+" " + times

        # s_date = datetime.datetime.strptime(starting_date, "%d-%m-%Y  %H:%M:%S")
        # print(s_date)
        # e_date = datetime.datetime.strptime(ending_date, "%d-%m-%Y  %H:%M:%S")
        # print(e_date)

        if RequirementForm.objects.filter(Q(id=req) & Q(project_id=pro)).exists():
            val = RequirementForm.objects.filter(id=req).update(survey_topic=survey_topic, subject_line=subject_line, actual_survey_length=actual_survey_length, target_audience_type=target_audience_type, b2b_b2c_dropdowns=b2b_b2c_dropdowns,
                                                                target_audience_textbox=target_audience_textbox, de_dupe_needed=de_dupe_needed, live_survey_link=live_survey_link, test_survey_link=test_survey_link, project_id=pro, de_dupe_project_id=de_dupe_project_id)

            # Project.objects.filter(id=pro).update(status='Active')

            clock = ProjectScheduler.objects.filter(project_id=pro).values()
            for i in clock:
                print(i)
                shedule = ClockedSchedule.objects.filter(
                    id=i['clock_id']).delete()

            ############  update status to active ################
            # shedule_start = ClockedSchedule.objects.create(
            #     clocked_time=s_date)  # "2021-11-22 17:37:00"
            # task_start = PeriodicTask.objects.create(name="updating_project_start"+str(pro), task="robas.task.project_task_active",
            #                                          clocked_id=shedule_start.id, one_off=True, args=json.dumps([pro]))
            # project_scheduler_start = ProjectScheduler.objects.create(
            #     project_id=pro, clock_id=shedule_start.id, task_id=shedule_start.id)

            ############  update status to closed  ###############
            # shedule_end = ClockedSchedule.objects.create(clocked_time=e_date)
            # task_end = PeriodicTask.objects.create(name="updating_project_end"+str(pro), task="robas.task.project_task_closed",
            #                                        clocked_id=shedule_end.id, one_off=True, args=json.dumps([pro]))
            # project_scheduler_end = ProjectScheduler.objects.create(
            #     project_id=pro, clock_id=shedule_end.id, task_id=task_end.id)

            return Response({"result": {'client_live_link': live_survey_link, 'requirement_form': 'requirement form updated successfully'}})
        return Response({'result': {'error': 'requirement form or project not found to update'}}, status=HTTP_404_NOT_FOUND)

# print(uuid.uuid4().hex[:10])

@method_decorator([authorization_required], name='dispatch')
class ExternalSamplingApiView(GenericAPIView):
    def get(self, request):
        if request.query_params:
            val = ExternalSampling.objects.filter(supplier_id=request.query_params['supplier_id'], project_id=request.query_params['project_id']).values()
            return Response({'result': val})
        # if pk:
        #     if ExternalSampling.objects.filter(id=pk).exists():
        #         val = ExternalSampling.objects.filter(id=pk).values()
        #         return Response({'result': {'external_sampling': val}})
        #     else:
        #         return Response({'error': {'message': 'external_sampling not found'}}, status=HTTP_404_NOT_FOUND)

    def put(self, request):
        data  = request.data
        complete_link = data['complete_link']
        quotas_full_link = data['quotas_full_link']
        terminated_link = data['terminated_link']
        client_quality_fail_link = data['client_quality_fail_link']
        panel_duplicate_link = data['panel_duplicate_link']
        project_id = data['project_id']
        supplier_id = data['supplier_id']

        if ExternalSampling.objects.filter(Q(project_id=project_id) & Q(supplier_id=supplier_id)).exists():
            ExternalSampling.objects.filter(project_id=project_id ,supplier_id=supplier_id).update(
                complete_link=complete_link, quotas_full_link=quotas_full_link, terminated_link=terminated_link,client_quality_fail_link=client_quality_fail_link, panel_duplicate_link=panel_duplicate_link, project_id=project_id, supplier_id=supplier_id
            )

            return Response({'message': 'external sample updated successfully'})
        return Response({'message': 'error'})

    def post(self, request):
        data = request.data

        complete_link = data['complete_link']
        quotas_full_link = data['quotas_full_link']
        terminated_link = data['terminated_link']
        client_quality_fail_link = data['client_quality_fail_link']
        panel_duplicate_link = data['panel_duplicate_link']
        project_id = data['project_id']
        supplier_id = data['supplier_id']

        if Project.objects.filter(id=project_id).exists():
            ext_sam = ExternalSampling.objects.create(complete_link=complete_link, quotas_full_link=quotas_full_link, terminated_link=terminated_link,
                                                      client_quality_fail_link=client_quality_fail_link, panel_duplicate_link=panel_duplicate_link, project_id=project_id, supplier_id=supplier_id)
            masked_url_data = []
            supplier_ids = {}
            a=SupplierMaskedLink.objects.all()
            print(a,'llll')

            if SupplierMaskedLink.objects.filter(Q(supplier_id=supplier_id) & Q(project_id=project_id)).exists():
                return Response({'error': "masked url is already exist for this suppliers"}, status=HTTP_406_NOT_ACCEPTABLE)
            else:
                req_id = RequirementForm.objects.get(project_id=project_id).id

                masked_url_for_supplier = "https://instantinsightz.com/pid="+str(project_id)+"&sid="+str(supplier_id)+"&mid="+str(uuid.uuid4().hex)+"&vid=XXXX"
                    
                supplier_masked_links = SupplierMaskedLink.objects.create(
                            supplier_id=supplier_id, masked_link=masked_url_for_supplier, project_id=project_id)
                    
                supplier = Supplier.objects.get(id=supplier_id).Supplier_Name
                supplier_ids['supplier_name'] = supplier
                supplier_ids['masked_url'] = masked_url_for_supplier
                masked_url_data.append(supplier_ids)
                supplier_ids = {}

                return Response({'result': {'masked_link': masked_url_data, 'external_samplig_id': ext_sam.id}, 'message': 'external sampling created successfully'})
        return Response({'error': {'message': 'project not found'}}, status=HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class SupplierMaskedLinks(APIView):
    def get(self, request):
        project_id = request.query_params['project_id']
        supplier_masked_link_obj = SupplierMaskedLink.objects.filter(project_id=project_id).values()
        final_list = []
        final_dict = {}
        for s in supplier_masked_link_obj:
            final_dict['masked_url'] = s['masked_link']
            supplier_obj = Supplier.objects.filter(id=s['supplier_id']).values()
            for i in supplier_obj:
                final_dict.update({'supplier_name': i['Supplier_Name']})
                final_dict.update({'supplier_id': i['id']})
            final_list.append(final_dict)
            final_dict = {}

        print(final_list)
        return Response({'result': final_list})

@method_decorator([authorization_required], name='dispatch')
class TemplateView(GenericAPIView):
    def get(self, request):
        val = Template.objects.all().values()
        company_id = request.query_params.get('company_id')
        type = request.query_params.get('type')
        if company_id != None:
            test1 = Template.objects.filter(
                Q(company=company_id) & Q(type=type)).values()
            return Response({'result': test1})
        return Response({'result': {'template': val}})

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        design = data.get('design')
        company = data.get('company')
        type = data.get('type')

        if Template.objects.filter(name=name).exists():
            return Response({'result': {'error': 'Name already exists'}}, status=HTTP_404_NOT_FOUND)

        else:
            Template.objects.create(
                name=name, design=design, company=company, type=type)
            return Response({'result': {'template': 'template created successfully'}})

@method_decorator([authorization_required], name='dispatch')
class ProjectRedirectView(generics.ListCreateAPIView):
    serializer_class = ProjectRedirectsSerializer
    queryset = ProjectRedirects.objects.all()


class ProjectRedirectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectRedirectsSerializer
    queryset = ProjectRedirects.objects.all()

@method_decorator([authorization_required], name='dispatch')
class SupplierApiView(ListAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    # pagination_class = MyPagination

    # def get(self,request):
    #     all_values = Supplier.objects.all().values()
    #     return Response({"Result":{'Supplier': all_values}})

    def post(self, request):
        data = request.data
        Supplier_Name = data.get('Supplier_Name')
        Contact_Person = data.get('Contact_Person')
        Methodology = data.get('Methodology')
        Email = data.get('Email')
        Billing_Email = data.get('Billing_Email')
        Website = data.get('Website')
        Phone = data.get('Phone')
        Status = data.get('Status')
        Total_Projects = data.get('Total_Projects')
        Total_Completes = data.get('Total_Completes')
        Avg_Vendor_Rating = data.get('Avg_Vendor_Rating')
        Payment_Term = data.get('Payment_Term')
        MSA = data.get('MSA')
        NDA = data.get('NDA')
        GDPR = data.get('GDPR')
        Vendor_Remarks = data.get('Vendor_Remarks')
        Avg_CPC = data.get('Avg_CPC')
        Audience = data.get(' Audience')
        is_for_project = data['is_for_project']

        if Supplier.objects.filter(Email=Email).exists():
            return Response({'result': {'error': 'email already exists'}}, status=HTTP_404_NOT_FOUND)

        else:

            test = Supplier.objects.create(Supplier_Name=Supplier_Name, Contact_Person=Contact_Person, Methodology=Methodology, Email=Email,
                                           Billing_Email=Billing_Email, Website=Website, Phone=Phone, Status=Status,
                                           Total_Projects=Total_Projects, Total_Completes=Total_Completes, Avg_Vendor_Rating=Avg_Vendor_Rating,
                                           Payment_Term=Payment_Term, MSA=MSA, NDA=NDA, GDPR=GDPR, Vendor_Remarks=Vendor_Remarks,
                                           Avg_CPC=Avg_CPC, Audience=Audience, is_for_project=is_for_project)

            return Response({'result': {'supplier': 'supplier created successfully'}})

@method_decorator([authorization_required], name='dispatch')
class SupplierUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    def get(self, request, pk):
        if Supplier.objects.filter(id=pk).exists():
            val = Supplier.objects.filter(id=pk).values()
            return Response({'result': {'supplier': val}})
        return Response({'error': {'supplier': 'Supplier Not Found'}}, status=HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data
        Supplier_Name = data.get('Supplier_Name')
        Contact_Person = data.get('Contact_Person')
        Methodology = data.get('Methodology')
        Email = data.get('Email')
        Billing_Email = data.get('Billing_Email')
        Website = data.get('Website')
        Phone = data.get('Phone')
        Status = data.get('Status')
        Total_Projects = data.get('Total_Projects')
        Total_Completes = data.get('Total_Completes')
        Avg_Vendor_Rating = data.get('Avg_Vendor_Rating')
        Payment_Term = data.get('Payment_Term')
        MSA = data.get('MSA')
        NDA = data.get('NDA')
        GDPR = data.get('GDPR')
        Vendor_Remarks = data.get('Vendor_Remarks')
        Avg_CPC = data.get('Avg_CPC')
        Audience = data.get(' Audience')
        is_for_project = data['is_for_project']

        if Supplier.objects.filter(id=pk).exists():
            test = Supplier.objects.filter(id=pk).update(Supplier_Name=Supplier_Name, Contact_Person=Contact_Person, Methodology=Methodology, Email=Email,
                                                         Billing_Email=Billing_Email, Website=Website, Phone=Phone, Status=Status,
                                                         Total_Projects=Total_Projects, Total_Completes=Total_Completes, Avg_Vendor_Rating=Avg_Vendor_Rating,
                                                         Payment_Term=Payment_Term, MSA=MSA, NDA=NDA, GDPR=GDPR, Vendor_Remarks=Vendor_Remarks,
                                                         Avg_CPC=Avg_CPC, Audience=Audience,is_for_project=is_for_project)

            return Response({'result': {'supplier': 'supplier updated successfully'}})
        return Response({'error': {'supplier': 'supplier not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Supplier.objects.filter(id=pk).exists():
            Supplier.objects.filter(id=pk).delete()
            return Response({'result': {'supplier': "supplier deleted successfully"}})
        return Response({'result': {'error': 'supplier not found'}}, status=HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class EmailTemplateAPI(APIView):
    def delete(self, request, pk):
        if EmailTemplate.objects.filter(id=pk).exists():
            EmailTemplate.objects.filter(id=pk).delete()
            return Response({'message': 'template is deleted successfully'})
        return Response({'err': 'template id not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data

        name = data['name']
        subject = data['subject']
        media_type = data['media_type']
        sender = data['sender']
        category = data['category']
        event_type = data['event_type']
        portal_name = data['portal_name']
        content = data['content']
        placeholder = data['placeholder']

        email_template = EmailTemplate.objects.create(name=name, subject=subject, media_type=media_type, sender=sender,
                                                      category=category, event_type=event_type, portal_name=portal_name, content=content, placeholder=placeholder)

        return Response({'result': {'email-template': 'template created successfully'}})

@method_decorator([authorization_required], name='dispatch')
class ThemeAPI(APIView):
    def get(self, request):
        theme_id = request.query_params.get('id')
        res = Theme.objects.filter(id=theme_id).values()
        return Response({"result": res})

    def post(self, request):
        data = request.data

        name = data.get('name')
        language = data.get('language')
        portal_name = data.get('portal_name')
        upload_css = data.get('upload_css')
        upload_image = data.get('upload_image')
        default_theme = data.get('default_theme')

        theme = Theme.objects.create(name=name, language=language, portal_name=portal_name,
                                     upload_css=upload_css, upload_image=upload_image, default_theme=default_theme)

        return Response({'result': {'theme': 'theme created successfully'}})

@method_decorator([authorization_required], name='dispatch')
class SelectEventType(GenericAPIView):
    def post(self, request):
        data = request.data

        event_type_name = data['event_type_name']

        val = getEventType(self, event_type_name)
        final_data = []
        data = {}
        for i in val:
            data['placeholder'] = i
            final_data.append(data)
            data = {}
        return Response({'result': final_data})


def getEventType(self, event_type_name):
    print(event_type_name)
    switcher = {
        "user_creation": ['#FirstName#', '#LastName#', '#Email#', '#Password#'],
        "forgot_password": ['#FirstName#', '#LastName#', '#Email#', '#Password#'],
        "change_password": ['#FirstName#', '#LastName#', '#Email#', '#Password#'],
        "panelist_registraion": ['#DateOfBirth#', '#DateOfJoining#', '#Email#', '#FirstName#', '#Gender#', '#Last_name#', '#LanguagePreference#', '#MobileNumber#', '#Password#', '#Id#', '#Link#', '#Otp#'],
        "send_out": ['#CampaignUrl#',  '#Points#',  '#ConversionRate#',  '#CampaignName#',  '#CampaignId#',  '#CampaignEndDate#', '#PanelistPassword#',  '#AvailablePoints#',  '#CampaignEmailOpenUrl#'],
        "faq": ['#Body#',  '#Subject#',  '#Email#',  '#FirstName#',  '#Last_name#',  '#Id#'],
        "project_details": ['#ProjectId#', '#ProjectName#', '#SMName1#', '#SMName2#', '#UpdateFields#', '#ModifiedBy#', '#ModifiedOn#'],
        "invite_survey": ['#SurveyId#', '#SurveyTopic#', '#Points#', '#SurveyEndDate#', '#SurveyUrl#', '#PanelistEmailId#', '#PanelistPassWord#',  '#AvailablePoints#', '#PanelistId#', '#ConversionRate#', '#TandC#', '#PrivacyPolicy#', '#UnSubscribe#', '#ProjectId#', '#EmailOpenUrl#', '#PortUrl#', '#UniqueId#'],
        "panelist_incentive": ['#TransactionDate#',  '#VoucherCode#', '#Amount#', '#Points#', '#PIN#', '#ExpiryDate#', '#DrawName#', '#NoOfTickets#', '#TicketId#', '#Name#', '#PanelistId#', '#TrackId1#', '#Name1#', '#PanelistId1#', '#AvailablePoints#', '#PointsExpiry#', '#Date#', '#CountryName#', '#Name2#', '#TrackId2#'],
    }
    return switcher.get(event_type_name)

def redirectExternalSurveyStatus(link):
    return redirect(link)

now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
print("cuurent time==>",current_time)
# start_time = "11:59:00"
# end_time = "2:00:00"

# start_times =datetime.datetime.strptime(start_time, "%H:%M:%S")
# end_times =datetime.datetime.strptime(end_time, "%H:%M:%S")

# print('end_times', now.time())

# delta = end_times - start_times

# print("total seconds==>",delta.total_seconds())

import socket   


class SampleStatus(APIView):
    def post(self, request):
    
        
        data = request.data
        print("printing vendor id true or false==>", request.session['vid'], data['status'])

        h_name = socket.gethostname()
        IP_addres = socket.gethostbyname(h_name)

        ip_address = ""

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            ip_address = str(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            ip_address = str(ip)

        if request.session['vid'] == True:
            supplier_id = request.session['supplier_id']

            # print("supplier_id= in sample status", supplier_id)
            # print("printd sandesh  project -id",data, data['pid'])
            if(IESamplingStatus.objects.filter(user_id=data['uid'], supplier_id=supplier_id).exists()):
                # print('coming to if block supplier id is', supplier_id)
                url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).terminated_link)
                updated_url = url.replace('<#id#>', request.session['client_transaction_id'])

                return Response(updated_url)
            else:
                print('coming to else block supplier id is', supplier_id)
                os_with_version =  request.user_agent.os.family+request.user_agent.os.version_string

                extermnal_start_time = request.session['external_start_time']
                now = datetime.datetime.now()
                external_end_current_time = now.strftime("%H:%M:%S")

                hostname=socket.gethostname()   
                IPAddr=socket.gethostbyname(hostname)   

                IESamplingStatus.objects.create(user_id=data['uid'], project_id=int(data['pid']), status=data['status'], IE='external', os=os_with_version, browser=request.user_agent.browser.family, supplier_id=supplier_id, client_id=data['uid'], survey_start_time =extermnal_start_time,survey_end_time=external_end_current_time, vendor_tid = request.session['client_transaction_id'], ip_adress=ip_address) 

                if(data['status'] == 'completed'):
                    print("1")
                    url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).complete_link)
                    updated_url = url.replace('<#id#>', request.session['client_transaction_id'])

                    total_complete = ProjectDashboard.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).complete
                    ProjectDashboard.objects.filter(project_id=int(data['pid']), supplier_id=supplier_id).update(complete=int(total_complete)+1)

                    return Response(updated_url)
                if(data['status'] == 'terminated'):
                    print("2")
                    url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).terminated_link)
                    updated_url = url.replace('<#id#>', request.session['client_transaction_id'])

                    total_terminated = ProjectDashboard.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).terminated
                    ProjectDashboard.objects.filter(project_id=int(data['pid']), supplier_id=supplier_id).update(complete=int(total_terminated)+1)

                    return Response(updated_url)
                if(data['status'] == 'qualityFailed'):
                    print("3")
                    url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).client_quality_fail_link)
                    updated_url = url.replace('<#id#>',  request.session['client_transaction_id'])

                    total_quality_fails = ProjectDashboard.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).quality_fail
                    ProjectDashboard.objects.filter(project_id=int(data['pid']), supplier_id=supplier_id).update(complete=int(total_quality_fails)+1)
                    
                    print("quality fail url==>>", updated_url)
		     
                    return Response(updated_url)
                if(data['status'] == 'panelDuplicate'):
                    print("4")
                    url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).panel_duplicate_link)
                    updated_url = url.replace('<#id#>', request.session['client_transaction_id'])

                    total_panel_duplicate = ProjectDashboard.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).panel_duplicate
                    ProjectDashboard.objects.filter(project_id=int(data['pid']), supplier_id=supplier_id).update(complete=int(total_panel_duplicate)+1)

                    return Response(updated_url)
                if(data['status'] == 'quotasFull'):
                    print("5")
                    print("coming to quotas full here ==<<..")
                    print("obj===>>",ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id))
                    url = str(ExternalSampling.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).quotas_full_link)
                    updated_url = url.replace('<#id#>',  request.session['client_transaction_id'])

                    total_quotas_full = ProjectDashboard.objects.get(project_id=int(data['pid']), supplier_id=supplier_id).quotas_full
                    ProjectDashboard.objects.filter(project_id=int(data['pid']), supplier_id=supplier_id).update(complete=int(total_quotas_full)+1)

                    

                    return Response(updated_url)

            return Response({'data': 'success'})

        if request.session['vid'] == False:
            hashids = Hashids(min_length=8)
            ints = hashids.decode(str(data['uid']))
            descrypted_uid = list(ints)[0]


            # ------------------- checking condition for quality fail ---------------------------

            now = datetime.datetime.now()
            end_current_time = now.strftime("%H:%M:%S")

            start_time = datetime.datetime.strptime(request.session['start_time'], "%H:%M:%S")

            end_time = datetime.datetime.strptime(end_current_time, "%H:%M:%S")

            total_second = end_time - start_time

            print("total seconds==>",total_second.total_seconds())

            length_of_interview = request.session['length_of_interview']

            print((int(length_of_interview) * 5/100) * 60)

            

            # ---------------------------------------------------------------------------------------

            hashids = Hashids(min_length=8)
            ints = hashids.decode(str(data['uid']))
            descrypted_uid = list(ints)[0]

            descrypted_uid = list(ints)[0]


            print("user id =============================>",  descrypted_uid)

            url = request.session['offer_url'].replace(data['uid'], str(descrypted_uid))
            sample_obj = Sampling.objects.filter(project_id=int(data['pid'])).values().last()

            if(IESamplingStatus.objects.filter(user_id=descrypted_uid).exists()):
                campaign_id = UserSurvey.objects.get(id=descrypted_uid).campaign_id

                os_with_version =  request.user_agent.os.family+request.user_agent.os.version_string

                user_obj = UserSurvey.objects.get(id=descrypted_uid)
                
                IESamplingStatus.objects.filter(user_id=descrypted_uid, project_id=int(data['pid']), IE='internal').update(status=data['status'], campaign_id=campaign_id, survey_end_time=end_current_time, browser=request.user_agent.browser.family , os=os_with_version, ip_adress=ip_address, user_country=user_obj.country)   

                # url = request.session['offer_url'].replace(data['uid'], str(descrypted_uid))

                # 500

                sample_obj = Sampling.objects.filter(project_id=int(data['pid'])).values().last()
                print("sample_obj", sample_obj)

                # print("session url=>"+ request.session['offer_url'], descrypted_uid)
                # print("url=>"+ url)

                # request.user_agent.os
                # request.user_agent.browser.family

                # IESamplingStatus.objects.filter(user_id=descrypted_uid).update(survey_end_time=datetime.datetime.now(), browser=request.user_agent.browser.family , os=os_with_version, ip_adress="", user_country=user_obj.country)

                UserSurveyOffers.objects.filter(user_survey_id=descrypted_uid, offer_link=request.session['offer_url']).update(is_attened=True, attened_date_time=datetime.datetime.now(), status=data['status'])

                if (int(length_of_interview) * 5/100) * 60 < total_second.total_seconds():

                    oldUserpoints = UserSurveyPoints.objects.get(user_survey_id=descrypted_uid)

                    total_points = int(oldUserpoints.points_earned) +  int(sample_obj['bonus_points'])
                    # 700

                    total_points_earned = UserSurveyPoints.objects.filter(user_survey_id=descrypted_uid).update(points_earned=total_points)

                    available_points = int(total_points) - int(oldUserpoints.points_spent) 

                    UserSurveyPoints.objects.filter(user_survey_id=descrypted_uid).update(available_points=available_points)
                else:
                    print('quality failed')
                    return Response({'result': 'success', 'status': 'quality failed', 'url': url, 'bonus_points': int(sample_obj['bonus_points'])})

                return Response({'result': 'success', 'status': data['status'], 'url': url, 'bonus_points': int(sample_obj['bonus_points'])})
            else:
                pass

        # return Response({'result': 'success'})

@method_decorator([authorization_required], name='dispatch')
class ProjectDashboardView(APIView):
    def get(self, request, pid):

        internal_dataData = []
        externalListData = []
        overAllCountOfExternal = {}
        total_completes_of_externalData = ""

        project_name = Project.objects.get(id=pid).name
        

        #  external sample data #

        # if ProjectDashboard.objects.filter(project_id=pid, ie='external').exists():

            # external_sample_obj = ExternalSampling.objects.filter(project_id=pid).values('supplier_id', 'supplier__Supplier_Name')
            

            # externalDict = {}
            # externalList = []

            # total_completes_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='completed').count()
            # total_terminated_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='terminated').count()
            # total_qualityFailed_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='qualityFailed').count()
            # total_quotasFull_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='quotasFull').count()
            # total_panelDuplicate_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='panelDuplicate').count()
            
            # overAllCountOfExternal = {
            #     'total_completes_of_external': total_completes_of_external,
            #     'total_terminated_of_external': total_terminated_of_external,
            #     'total_qualityFailed_of_external': total_qualityFailed_of_external,
            #     'total_quotasFull_of_external': total_quotasFull_of_external,
            #     'total_panelDuplicate_of_external': total_panelDuplicate_of_external
            # } 
            # total_completes_of_externalData = overAllCountOfExternal

            # for i in external_sample_obj:
            #     # i['supplier_id']
            #     external_total_complete = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='completed')
            #     external_total_quality_fail = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='qualityFailed')
            #     external_total_quotas_full = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='quotasFull')
            #     external_total_panel_duplicate = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='panelDuplicate')
            #     external_total_terminated = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='terminated')

            #     externalDict['supplier_name'] =  i['supplier__Supplier_Name']
            #     externalDict['completes'] = external_total_complete.count()
            #     externalDict['quality_fail'] = external_total_quality_fail.count()
            #     externalDict['terminated'] = external_total_terminated.count()
            #     externalDict['quotas_full'] = external_total_quotas_full.count()
            #     externalDict['panel_dupicate'] = external_total_panel_duplicate.count()
            #     externalList.append(externalDict)
            #     externalDict = {}

            # externalListData = externalList
            
            # final_data = {'external': externalList, 'overAllExternalCount':overAllCountOfExternal, 'project_name': project_name}
        

        # internal data #
        if ProjectDashboard.objects.filter(project_id=pid, ie='internal').exists():
            rr = ProjectDashboard.objects.get(project_id=pid, ie='internal').response_rate
            total_invite_sent = ProjectDashboard.objects.get(project_id=pid, ie='internal').total_invite_sent
            total_spent = ProjectDashboard.objects.get(project_id=pid,ie='internal').total_spent
            total_clicks = UserClicks.objects.filter(project_id=pid, is_clicked=True).count()

            internal_total_count = IESamplingStatus.objects.filter(project_id=pid, IE='internal').count()
            internal_completed = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='completed').count()
            internal_terminated = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='terminated').count()
            internal_quotas_full = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='quotasFull').count()
            internal_quality_fail = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='qualityFailed').count()
            internal_panel_duplicate = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='panelDuplicate').count()

            internal_data = [{
                'total_clicks': total_clicks,
                'completed': internal_completed,
                'terminated': internal_terminated,
                'quotas_full': internal_quotas_full,
                'quality_fail': internal_quality_fail,
                'panel_duplicate': internal_panel_duplicate,
                'response_rate': rr,
                'total_invite_sent': total_invite_sent,
                'total_spent': total_spent
            }]

            internal_dataData = internal_data

            final_data = {'internal': internal_data, 'overAllExternalCount':overAllCountOfExternal, 'project_name': project_name}
        
        else:
            external_sample_obj = ExternalSampling.objects.filter(project_id=pid).values('supplier_id', 'supplier__Supplier_Name')
            

            externalDict = {}
            externalList = []

            total_completes_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='completed').count()
            total_terminated_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='terminated').count()
            total_qualityFailed_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='qualityFailed').count()
            total_quotasFull_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='quotasFull').count()
            total_panelDuplicate_of_external = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='panelDuplicate').count()
            
            overAllCountOfExternal = {
                'total_completes_of_external': total_completes_of_external,
                'total_terminated_of_external': total_terminated_of_external,
                'total_qualityFailed_of_external': total_qualityFailed_of_external,
                'total_quotasFull_of_external': total_quotasFull_of_external,
                'total_panelDuplicate_of_external': total_panelDuplicate_of_external
            } 
            total_completes_of_externalData = overAllCountOfExternal

            for i in external_sample_obj:
                # i['supplier_id']
                external_total_complete = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='completed')
                external_total_quality_fail = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='qualityFailed')
                external_total_quotas_full = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='quotasFull')
                external_total_panel_duplicate = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='panelDuplicate')
                external_total_terminated = IESamplingStatus.objects.filter(project_id=pid, IE='external', supplier_id=i['supplier_id'], status='terminated')

                externalDict['supplier_name'] =  i['supplier__Supplier_Name']
                externalDict['completes'] = external_total_complete.count()
                externalDict['quality_fail'] = external_total_quality_fail.count()
                externalDict['terminated'] = external_total_terminated.count()
                externalDict['quotas_full'] = external_total_quotas_full.count()
                externalDict['panel_dupicate'] = external_total_panel_duplicate.count()
                externalList.append(externalDict)
                externalDict = {}

            externalListData = externalList
            
            final_data = {'external': externalList, 'overAllExternalCount':overAllCountOfExternal, 'project_name': project_name}

        
        final_data = {'internal': internal_dataData, 'external': externalListData, 'overAllExternalCount':overAllCountOfExternal, 'project_name': project_name}

        return Response(final_data)


        # internal_sample = ProjectDashboard.objects.filter(project_id=pid, ie='internal').values()

        # external_sample = ProjectDashboard.objects.filter(project_id=pid, ie='external').values(
        #     'terminated' ,'quotas_full', 'quality_fail', 'panel_duplicate', 'complete', 'supplier_id__Supplier_Name'
        # )
        # c = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='completed').count()
        # t = IESamplingStatus.objects.filter(project_id=pid, IE='external', status='terminated').count()
        # return Response({'result': internal_sample,'external_sample_data': external_sample, 'total_compltes': c, 'total_terminate': t})



    #     if ProjectDashboard.objects.filter(project_id=pid, ).exists():

    #         ie_sampling_obj_completed = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='completed').count()
    #         terminated = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='terminated').count()
    #         quotas_full = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='quotasFull').count()
    #         quality_fail = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='qualityFailed').count()
    #         panel_duplicate = IESamplingStatus.objects.filter(project_id=pid, IE='internal', status='panelDuplicate').count()

    #         invite_sent = ProjectDashboard.objects.get(project_id=pid).total_invite_sent
    #         completion_rate = ie_sampling_obj_completed / invite_sent
    #         ProjectDashboard.objects.filter(project_id=pid).update(complete=ie_sampling_obj_completed, completion_rate=completion_rate, quotas_full=quotas_full, terminated=terminated, quality_fail=quality_fail, panel_duplicate=panel_duplicate)
    #         obj = ProjectDashboard.objects.filter(project_id=pid).values()
    #         project_name = ProjectDashboard.objects.filter(project_id=pid).values('project__name')

    #         external_sample = [{
    #             'ext_completed' : IESamplingStatus.objects.filter(project_id=pid, IE='external', status='completed').count(),
    #             'ext_terminated' : IESamplingStatus.objects.filter(project_id=pid, IE='external', status='terminated').count(),
    #             'ext_quotas_full' : IESamplingStatus.objects.filter(project_id=pid, IE='external', status='quotasFull').count(),
    #             'ext_quality_fail' : IESamplingStatus.objects.filter(project_id=pid, IE='external', status='qualityFailed').count(),
    #             'ext_panel_duplicate' : IESamplingStatus.objects.filter(project_id=pid, IE='external', status='panelDuplicate').count()
    #         }]


    #         return Response({'result': obj, 'external_sample_data': external_sample, 'project_name': project_name, 'supplier_name': SupplierMaskedLink.objects.filter(project_id=pid).values('supplier__Supplier_Name')})
    #     return Response({'error': 'project not found'})



import itertools
from usersurvey.models import *

import csv
import openpyxl

import base64


class RemoveUserPointsByExcelUploads(APIView):
    def post(self, request):
        name = request.data['name']
        excel_file = request.data['excel_file']

        split_base_url_data = excel_file.split(';base64,')[1]
        excel_file_decoded = base64.b64decode(split_base_url_data)


        filename1 = "/instantInsight/site/public/media/consolidated_project/"+name+'.xlsx'
        fname1 = '/consolidated_project/'+name+'.xlsx'
        ss=  open(filename1, 'wb')
        print("sss==>>>",ss)
        ss.write(excel_file_decoded)
        ss.close()   

        # excel_file = request.FILES.get('points_excel_file')

        # print('coming excel file', excel_file)

        # if not excel_file.name.endswith('.csv'):
        #     return Response({'Result': {'Error': 'File Format should be csv'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        dataframe = pd.read_excel(filename1)

        print("dataframe==>", dataframe)


        lit_of_user = [item for item in  dataframe['user id'].tolist()]
        lit_of_points = [item for item in  dataframe['points to remove'].tolist()]
        # print("lit_of_user_id==>",lit_of_user) 
        for (a, b) in itertools.zip_longest(lit_of_user, lit_of_points):
            print (a, b)
            user_pints = UserSurveyPoints.objects.get(user_survey_id=a)  
            # print(user_pints.points_earned)
            
            points_earned = user_pints.points_earned  #50

            after_deduction = int(points_earned) - int(b)  # 30
            # 50 - 20 = 30 

            available_points = user_pints.available_points - int(b)
            user_pints = UserSurveyPoints.objects.filter(user_survey_id=a).update(points_earned = after_deduction, available_points = available_points)

        return Response({'message': 'file uploaded successfully'})

