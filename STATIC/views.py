from pprint import pprint
import re
from typing import Any
from django.db.models.aggregates import Count
from django.db.models.expressions import Case
from django.http import HttpResponseRedirect
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

import datetime
from django.utils import timezone
import json
import secrets  
from projects.pagination import MyPagination
from account.models import Company
from bs4 import BeautifulSoup


from surveyQuestionare.models import *




# Create your views here.


class CampaignTypeView(ListAPIView):
    serializer_class = CampaignTypeSerializer
    queryset = CampaignType.objects.all()
    pagination_class = MyPagination
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
    pagination_class = MyPagination
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

import itertools

class CampaignView(ListAPIView):
    # serializer_class = CampaignSerializer
    # queryset = Campaign.objects.all()
    # pagination_class = MyPagination

    def get(self, request, *args, **kwargs):
        values = Campaign.objects.all().values()
        for i, j in itertools.zip_longest(values, range(len(values))):
            company = Company.objects.get(id=i['company_id'])
            campaign_type = CampaignType.objects.get(id=i['campaign_type_id'])
            
            values[j]['comapany_name'] = company.name
            values[j]['campaign_type_name'] = campaign_type.name
               
        return Response({'result': values})

    def post(self, request, *args, **kwargs):
        data = request.data

        market_type = data['market_type']
        compaign_name = data['compaign_name']
        lead_required = data['lead_required']
        start_date = data['start_date']
        length_of_interview = data['length_of_interview']
        is_quality_follow_up = data['is_quality_follow_up']
        description = data['description']
        is_relevantld_check = data['is_relevantld_check']
        cpa = data['cpa']
        end_data = data['end_data']
        recruitment_type = data['recruitment_type']
        token = data['token']
        company_id = data['company_id']
        campaign_type = data['campaign_type']
        commision_model = data['commision_model']
        question_library_id = data.get('question_library_id')

        
        # r1 = random.randint(10, 100000)
        # unique_id = str(r1)
        # compaign_link = "https://robas.thestorywallcafe.com/="+str(unique_id)

        if CampaignType.objects.filter(id=campaign_type).exists():
            if CommissionModel.objects.filter(id=commision_model).exists():
                campaign = Campaign.objects.create(market_type=market_type, compaign_name=compaign_name, lead_required=lead_required, start_date=start_date, length_of_interview=length_of_interview, is_quality_follow_up=is_quality_follow_up, description=description, is_relevantld_check=is_relevantld_check,
                                        cpa=cpa, end_data=end_data, recruitment_type=recruitment_type,  token=token, company_id=company_id, campaign_type_id=campaign_type, commision_model_id=commision_model)

                compaign_link = "https://robas.thestorywallcafe.com/#/campaign-register?campaign_id="+str(campaign.id)
                survey_template_link = "https://robas.thestorywallcafe.com/#/surveyTemplate?campaign_id="+str(campaign.id)

                Campaign.objects.filter(id=campaign.id).update(compaign_link=compaign_link, surveyTemplate_link=survey_template_link)

                # if question_library_id is not None: 
                #     for questions in question_library_id:
                #         if QuestionLibrary.objects.filter(id=questions).exists():
                #             question_library = CampaignQuestionLibrary.objects.create(campaign_id=campaign.id, question_library_id=questions)
                #             print("=====",question_library.id)
                #         else:
                #             return Response({'error': {'message': 'question ids not found'}})

                return Response({'result': {'campaign_id': campaign.id, 'campaign_link': compaign_link}, 'message': 'campaign created successfully'})
            return Response({'result': {'error': 'no commision model found'}}, status=HTTP_404_NOT_FOUND)
        return Response({'result': {'error': 'no campaign type found'}}, status=HTTP_404_NOT_FOUND)

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
            questions['question_text'] = qst.question_text
            val.append(questions)
            questions = {}

        val2 = []
        page = {}
        pg_id =[]
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
        
        return Response({'questions': val, 'targeted_page': val2,}) 

class pixelCode(GenericAPIView):
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


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk):
        if Campaign.objects.filter(id=pk).exists():
            val = Campaign.objects.filter(id=pk).values()
            return Response({'result': {'campaign': val}})
        return Response({'result': {'error': 'no campaign found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Campaign.objects.filter(id=pk).exists():
            Campaign.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'campaign deleted successfully'}})
        return Response({'result': {'error': 'no compaign found to delete'}}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        data = request.data

        market_type = data['market_type']
        compaign_name = data['compaign_name']
        lead_required = data['lead_required']
        start_date = data['start_date']
        length_of_interview = data['length_of_interview']
        is_quality_follow_up = data['is_quality_follow_up']
        description = data['description']
        is_relevantld_check = data['is_relevantld_check']
        cpa = data['cpa']
        end_data = data['end_data']
        recruitment_type = data['recruitment_type']
        token = data['token']
        company_id = data['company_id']
        campaign_type = data['campaign_type']
        commision_model = data['commision_model']

        value = Campaign.objects.filter(id=pk).exists()

        if CampaignType.objects.filter(id=campaign_type).exists():
            if CommissionModel.objects.filter(id=commision_model).exists():
                if value:
                    c_link = Campaign.objects.get(id=pk).compaign_link
                    Campaign.objects.filter(id=pk).update(market_type=market_type, compaign_name=compaign_name, lead_required=lead_required, start_date=start_date, length_of_interview=length_of_interview, is_quality_follow_up=is_quality_follow_up, description=description, is_relevantld_check=is_relevantld_check,
                                                          cpa=cpa, end_data=end_data, recruitment_type=recruitment_type, token=token, company_id=company_id, campaign_type_id=campaign_type, commision_model_id=commision_model)
                    return Response({'result': {'campaign_id': pk, 'campaign_link': c_link}, 'campaign': 'campaign_view updated successfully'})
                return Response({'result': {'error': 'no compaign found to update'}}, status=HTTP_404_NOT_FOUND)
            return Response({'result': {'error': 'no commision model found'}}, status=HTTP_404_NOT_FOUND)
        return Response({'result': {'error': 'no campaign type found'}}, status=HTTP_404_NOT_FOUND)


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

class CampaignSubmitApi(APIView):
    # serializer_class = UserSurveySerializer
    # queryset = UserSurvey.objects.all()
    # pagination_class = MyPagination

    def post(self, request):
        data = request.data

        campaign_id = data.get('campaign_id') #from formtend they has to stored from url and send id
        status= 'SOI'
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        gender = data.get('gender')
        DOB = data.get('DOB')
        # question_choice = data['question_choice']

        user_survey = UserSurvey.objects.create(first_name=first_name ,last_name=last_name ,email=email ,dob=DOB ,gender=gender, status=status)

        # if question_choice is not None:
        #     for i in range(len(question_choice)):
        #         question_id = question_choice[i]['question_id']
        #         answer_id = question_choice[i]['answer_id']

        #         ans_split = answer_id.split(',')
        #         for i in ans_split:
        #             print(i)
        #             data = Answer.objects.create(user_survey_id=user_survey.id ,answers=i, question_library_id=question_id)               

        camapaign_url = Campaign.objects.get(id=campaign_id).surveyTemplate_link
        url = camapaign_url+"&panelist_id="+str(user_survey.id)
        # print(url)
            
        html_path = 'verify-email.html'
        context_data = {'name': first_name, 'email': email, 'url': url}
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

        type = data.get('type')
        user_survey_id = data.get('user_survey_id')
        verified_data = data.get('verified_data')

        if UserSurvey.objects.filter(email=verified_data, id=user_survey_id).exists():
            UserSurvey.objects.filter(id=user_survey_id).update(status="DOI", is_email_verified=True)
            return redirect('')
            # return Response({'result': {'campaign verify': 'verified'}})
        return Response({'result': {'campaign verify':'campaign not verified'}})


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
        print(answer)
       
        question_name = QuestionLibrary.objects.get(id=question_id)
        operator = QuestionOperator.objects.filter(id=operator_id).values()
        for i in operator:
            print(i['name'])
        answers = Answer.objects.filter(answers=answer).values('answers')
        answers = QuestionChoice.objects.filter(id__in=answer).values()
        answerList = []
        for k in answers:
            print(k['name'])
            answerList.append(k['name'])

        # for j in answer:
        data = Answer.objects.filter(Q_object_creater(self ,question_id, operator_id, answer)).count()
        return Response({'result': {'count': data,  'question_name': question_name.question_name, 'operator': i['name'], 'answers': answerList}})

class BuildCriteria(APIView):
    def post(self, request):
        data = request.data  

        criterias = data.get('criteria')
        print(criterias)
        criteria_operator = data.get('criteria_operator')

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer']))
        for i in range(1, len(criterias)):
            print(i)
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'])
            query.add(q_object, operator.get(criteria_operator[i-1]))
        print(query)
        count_data = Answer.objects.filter(query).count()   
        print("count",count_data)
        
        data1 = Answer.objects.filter(query).values() 
        return Response({'result': {'count': count_data, 'requested_data': data}})

class DrawSamples(GenericAPIView):
    def post(self, request):
        data = request.data
        criterias = data.get('criteria')
        criteria_operator = data.get('criteria_operator')
        drawsample = data['drawsample']

        operator = {"AND": Q.AND, "OR": Q.OR, "NOT": Q.negate}
        query = Q(Q_object_creater(self ,criterias[0]['question_id'], criterias[0]['operator_id'], criterias[0]['answer']))
        for i in range(1, len(criterias)):
            print(i)
            q_object = Q_object_creater(self ,criterias[i]['question_id'], criterias[i]['operator_id'], criterias[i]['answer'])
            query.add(q_object, operator.get(criteria_operator[i-1]))
        count_data = Answer.objects.filter(query).count()   
        
        data1 = Answer.objects.filter(query).values() 

        emails = []
        
        for d in data1:
            d1 = UserSurvey.objects.get(id=d['user_survey_id'])
            emails.append(d1.email)
            # print(d1.email,"==",d1.id)
        
        secure_random = secrets.SystemRandom() 

        list_of_random_items = secure_random.sample(emails, drawsample)
        # print("random items",list_of_random_items)
        print(emails)

        return Response({'result': {'emails': list_of_random_items}})

class SendOut(APIView):
    def post(self, request):
        data = request.data 

        template_id = data.get('template_id')
        shedule = data['shedule']
        max_reminder_sent = data['max_reminder_sent']
        emails = data['emails']

        val = EmailTemplate.objects.get(id=template_id)
        
        sender = val.sender
        subject = val.subject

        email_body = val.content

        soup = BeautifulSoup(email_body, 'html')
        clss = soup.find("a", class_="targetPage")

        if shedule is None:
            for i in emails:
                print("emails", i)
                clss['href'] = Prescreener.objects.last().generated_link + str(UserSurvey.objects.get(email=i).panelist_id)
                em_body = soup.prettify()
                # send_email_task.delay(emails, sender, email_body, subject)                
                email = EmailMessage(subject, em_body, from_email=sender, to=['vignesh@ekfrazo.in'])
                email.content_subtype = "html"
                email.send(fail_silently=False)

        # print(query)
        if shedule is not None:

            string = shedule['date']+" "+ shedule['time']
            date = datetime.datetime.strptime(string, "%d-%m-%Y  %H:%M:%S")
            print(date)
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
            
            interval =  IntervalSchedule.objects.create(every=3, period='days')
            print(interval.id)

            task = PeriodicTask.objects.create(start_time=date_time, name="sending_email_to_paelist"+str(interval.id), task="robas.task.send_email_task", args=json.dumps([emails, sender, email_body, subject]), interval_id=interval.id)

            # print(schedule)
        return Response({'result': {'count': 'mail has been sent to all the panelist email ids'}})

class PanelistPrescreenerAnswer(APIView):
    def post(self, request):
        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        
        if PrescreenerSurvey.objects.filter(panelist_id=panelist_id).exists():
            return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            for i in answered_question:
                for j in i['option_id']:
                    data = PrescreenerSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j)
            return Response({'result': {'message': 'Thank you for your response'}})

class PanelistPeCampaignAnswer(APIView):
    def post(self, request):
        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        
        if PeCampaignSurvey.objects.filter(panelist_id=panelist_id).exists():
            return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            for i in answered_question:
                for j in i['option_id']:
                    data = PeCampaignSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j)
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

def Q_object_creater(self, question_id, operator_id, answer):
    print("answer fun:",answer)
    switcher = {
            1 : Q(question_library_id=question_id),  #is fill
            2 : ~Q(question_library_id=question_id),  #is not filled
            3 : Q(answers__iexact=answer) & Q(question_library_id=question_id), #is eqaul
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
    # return

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
                questions = QuestionLibrary.objects.filter(question_type_id=question_type, question_category_id=question_category).values('id', 'question_name')
                return Response({'result': {'questions': questions}})
            return Response({'error': {'message': 'question category not found'}}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': {'message': 'question type not found'}}, status=status.HTTP_404_NOT_FOUND)
        

#@@@@@@@@@@@@@@@@@  Build Creiteria @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class SelectQuestionForBuildCriteria(GenericAPIView):
    def post(self, request):
        data = request.data

        question_id = data['question_id']

        if QuestionLibrary.objects.filter(id=question_id).exists():
            qst = QuestionLibrary.objects.get(id=question_id)
            # print(qst.question_type_id)

            qst_choice = QuestionChoice.objects.filter(question_library_id=question_id).values()
            # print(qst_choice)

            answrs = []
            all_choice = {}
            for i in qst_choice:
                all_choice = {}
                # print(i)
                all_choice['choice_id'] = i['id']
                all_choice['name'] = i['name']

                answrs.append(all_choice)

            print("answers==",answrs)

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

    print(all_list)
    operators = {
        'Single Select': [all_list[0], all_list[1], all_list[6], all_list[7]],
        'Multiple Select': [all_list[0], all_list[1], all_list[6], all_list[7]],
        'Check Box': [all_list[0], all_list[1], all_list[6], all_list[7]],
        'Multiple Choice': [all_list[0], all_list[1], all_list[4], all_list[5], all_list[6], all_list[7]],
        'Plan Text': [all_list[2], all_list[3],all_list[6], all_list[7], all_list[8], all_list[9]],
        'Radio Button': [all_list[0], all_list[1], all_list[4], all_list[5], all_list[2], all_list[3]],
        # 'Date': [all_list[10], all_list[11], all_list[12], all_list[13], all_list[14], all_list[15],  all_list[16], all_list[17]],
    }
    # print(data)
    return operators.get(data)

class CampaignPageApiView(GenericAPIView):
    def get(self, request): 
        campaign_id = request.query_params['campaign_id']
#         print("quryparms===",campaign_id)

        if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).exists():
            res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id).values()
            # print(res)
            final_output = []


            page_id1 = []
            json_data = {'page_id': '','page_name': ''}
            for i in res:
                page_id1.append(i['page_id'])

            print("page_id1", page_id1) 
            page_id2 = list(dict.fromkeys(page_id1))
            print("page_id2", page_id2)   

            q_ids = []
            res2 = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id__in=page_id2).values('question_library_id')
            for j in res2:
                print(j)
                q_ids.append(j['question_library_id'])
            print("q_ids", q_ids)

            fpage = Page.objects.filter(id__in=page_id2).values()  
            for k in fpage:
                json_data['page_id'] = k['id']
                json_data['page_name'] = k['name']
                final_output.append(json_data)
                json_data = {}
            print("fpage", fpage)          
                    

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

class SurveyTemplateApiView(APIView):
    def get(self, request):
        prescreener_id = request.GET.get('prescreener_id')
        campaign_id = request.GET.get('campaign_id')
        pe_campaign_id = request.GET.get('pe_campaign_id')
        survey_questionare_id = request.GET.get('survey_questionare_id')

        if prescreener_id:
            pages_for_prescreener = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).values()
        
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
                for p in PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=k).values():
                    if(p['question_library_id']!= None):
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

        if campaign_id:
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



