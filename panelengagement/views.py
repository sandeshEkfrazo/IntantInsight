import base64
import io
from os import dup
from django.http import response
from django.shortcuts import render
from comman.models import *
from panelengagement.serializers import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
import csv
from django.http import HttpResponse
import time, datetime
from datetime import timedelta
from projects.pagination import MyPagination
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from django.conf import settings
from django.db.models import Q
from panelbuilding.views import questionType
from bs4 import BeautifulSoup
from django.shortcuts import redirect
from django.core.mail import EmailMessage, send_mail
from usersurvey.models import *
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
import json
from account.backends_ import *
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule, IntervalSchedule

@method_decorator([authorization_required], name='dispatch')
class PeCampaignListApiView(ListAPIView):
    serializer_class = PeCampaignSerializer
    queryset = PeCampaign.objects.all().order_by('-id')
    # pagination_class = MyPagination

@method_decorator([authorization_required], name='dispatch')
class RedemptionListApiView(ListAPIView):
    serializer_class = RedemptionSerializer
    queryset = Redemption.objects.all()
    # pagination_class = MyPagination

# class AllLogicsApiView(ListAPIView):
#     serializer_class = LogicSerializer
#     queryset = Logics.objects.all()

# class AllLogicTypeApiView(ListAPIView):
#     serializer_class = LogicTypeSerializer
#     queryset = LogicType.objects.all()

@method_decorator([authorization_required], name='dispatch')
class AllPageApiView(ListAPIView):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# class PeCampaignTypeView(ListAPIView):
#     serializer_class = PeCampaignTypeSerializer
#     queryset = PeCampaignType.objects.all()
#     pagination_class = MyPagination
#     # def get(self, request):
#     #     values = PeCampaignType.objects.all().values()
#     #     return Response({'Result': {'Pe Campaign Type': values}})

#     def post(self, request):
#         data = request.data
#         name = data['name']

#         if PeCampaignType.objects.filter(name=name).exists():
#             return Response({'result': {'error': 'name already taken'}})
#         PeCampaignType.objects.create(name=name)
#         return Response({'result': {'pe_campaign_type': 'pe campaign created successfully'}})

#     def delete(self, request, pk):
#         if PeCampaignType.objects.filter(id=pk).exists():
#             PeCampaignType.objects.filter(id=pk).delete()
#             return Response({'result': {'message': 'PeCampaignType deleted successfully'}})
#         return Response({'result': {'error': 'PeCampaignType id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

# class PeCategoryView(ListAPIView):
#     serializer_class = PeCategorySerializer
#     queryset = PeCategory.objects.all()
#     pagination_class = MyPagination
#     # def get(self, request):
#     #     values = PeCategory.objects.all().values()
#     #     return Response({'Result': {'Pe Category': values}})

#     def post(self, request):
#         data = request.data
#         name = data['name']

#         if PeCategory.objects.filter(name=name).exists():
#             return Response({'result': {'error': 'name already taken'}})
#         PeCategory.objects.create(name=name)
#         return Response({'result': {'pe_pategory': 'pe category created successfully'}})

#     def delete(self, request, pk):
#         if PeCategory.objects.filter(id=pk).exists():
#             PeCategory.objects.filter(id=pk).delete()
#             return Response({'result': {'message': 'PeCategory deleted successfully'}})
#         return Response({'result': {'error': 'PeCategory id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

class ISDeleteORstore(APIView):
    def post(self, request):
        data = request.data
        
        PeCampaign.objects.filter(id=data['campaign_id']).update(is_deleted=data['is_deleted_or_restored'])

        today = datetime.datetime.today()
        after_90_days = today + timedelta(days=89)

        if data['is_deleted_or_restored']:   #true

            clocked_obj = ClockedSchedule.objects.create(
                    clocked_time = after_90_days 
            )
            task_start = PeriodicTask.objects.create(name="DeletePeCampaignAutoAfter90Days"+str(clocked_obj.id), task="panelengagement.tasks.deletePeCampaign",clocked_id=clocked_obj.id, one_off=True, kwargs=json.dumps({'pe_campaign_id': data['campaign_id']}))

            return Response({'result': 'Campaign Deleted successfully'})
        else:
            cloked_id = PeriodicTask.objects.get(kwargs=json.dumps({'pe_campaign_id': data['campaign_id']})).clocked_id
            ClockedSchedule.objects.filter(id=cloked_id).delete()

            return Response({'result': 'Campaign Restored successfully'})

        return Response({'result': 'success'})

@method_decorator([authorization_required], name='dispatch')
class PeCampaignView(GenericAPIView):
    def get(self, request, pk):
        if PeCampaign.objects.filter(id=pk).exists():
            val = PeCampaign.objects.filter(id=pk).values(
                "market",
                "campaign_name",
                "points",
                "status",
                "profile_type",
                "external_profile_link",
                "internal_campaign_generated_link",
                "pe_category",
                "pe_campaign_type_id",
                "created_date",
                "updated_dateTime",
                "created_by",
                "updated_by",
                "is_deleted",
            )
            return Response({'result': {'pe_campaign': val}})
        return Response({'result': {'error': 'Not Found'}})
    
    def post(self, request):
        data = request.data
        market = data['market']
        campaign_name = data['campaign_name']
        points = data['points']
        status = data['status']
        # pe_category_id = data['pe_category_id']
        pe_campaign_type_id = data['pe_campaign_type_id']
        profile_type = data['profile_type']
        external_profile_link = data['external_profile_link']
        question_library_id = data.get('question_library_id')
        created_by = data['created_by']
        updated_by = data['updated_by']

        if PeCampaign.objects.filter(campaign_name=campaign_name).exists():
            return Response({'result': "Campaign name already taken"}, status=HTTP_400_BAD_REQUEST)

        if PeCampaignType.objects.filter(id=pe_campaign_type_id).exists():
            pe_campaign = PeCampaign.objects.create(market=market ,campaign_name=campaign_name ,points=points ,status=status ,pe_campaign_type_id=pe_campaign_type_id ,profile_type=profile_type ,external_profile_link=external_profile_link, created_by_id=created_by ,updated_by_id=updated_by)

            # if question_library_id is not None: 
            #     for questions in question_library_id:
            #         if QuestionLibrary.objects.filter(id=questions).exists():
            #             question_library = PeCampaignQuestionLibrary.objects.create(pe_campaign_id=pe_campaign.id, question_library_id=questions)
            #             print("=====",question_library.id)
            #         else:
            #             return Response({'error': {'message': 'question ids not found'}})

            generated_campaign_live_link = settings.LIVE_URL+"/pcid="+str(pe_campaign.id)
                # generated_campaign_live_link = "localhost:8000/pcid="+str(pe_campaign.id)

            PeCampaign.objects.filter(id=pe_campaign.id).update(internal_campaign_generated_link=generated_campaign_live_link)

            Page.objects.create(name="Thank You", pe_campaign_id=pe_campaign.id)
            Page.objects.create(name="Terminated", pe_campaign_id=pe_campaign.id)

            return Response({'result': {'pe_campaign_id': pe_campaign.id}, 'message': 'pe campaign created successfully'})    
        return Response({'result': {'error': 'no pe-campaign type found'}}, status=HTTP_404_NOT_FOUND)      
        # return Response({'result': {'error': 'no pe-category found'}}, status=HTTP_404_NOT_FOUND)  

    def put(self, request, pk):
        data = request.data
        market = data['market']
        campaign_name = data['campaign_name']
        points = data['points']
        status = data['status']
        # pe_category_id = data['pe_category_id']
        pe_campaign_type_id = data['pe_campaign_type_id']
        profile_type = data['profile_type']
        external_profile_link = data['external_profile_link']
        updated_by = data['updated_by']


        if PeCampaign.objects.filter(~Q(id=pk) & Q(campaign_name=campaign_name)).exists():
            return Response({'result': "Campaign name already taken"}, status=HTTP_400_BAD_REQUEST)


        # if PeCategory.objects.filter(id=pe_category_id).exists():
        if PeCampaignType.objects.filter(id=pe_campaign_type_id).exists():
            if PeCampaign.objects.filter(id=pk).exists():
                PeCampaign.objects.filter(id=pk).update(market=market ,campaign_name=campaign_name ,points=points ,status=status,pe_campaign_type_id=pe_campaign_type_id ,profile_type=profile_type ,external_profile_link=external_profile_link, updated_by_id=updated_by)
                return Response({'result': {'pe_campaign_id': pk}, 'message': 'pe-campaign updated successfully'})
            return Response({'result': {'error': 'no pe-campaign found'}}, status=HTTP_404_NOT_FOUND)      
        return Response({'result': {'error': 'no pe-campaign type found'}}, status=HTTP_404_NOT_FOUND)    
        # return Response({'result': {'error': 'no pe category found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if PeCampaign.objects.filter(id=pk).exists():
            val = PeCampaign.objects.filter(id=pk).delete()
            return Response({'result': {'pe campaign': 'deleted successfully'}})
        return Response({'result': {'error': 'no record found to delete'}}, status=status.HTTP_404_NOT_FOUND)  

import requests
from robas.encrdecrp import encrypt


@method_decorator([authorization_required], name='dispatch')
class AssingCamapigntoAllPanelist(APIView):
    def post(self, request):
        data = request.data

        # iv =  '1234567891011121'.encode('utf-8')
        hashids = Hashids(min_length=8)
        pe_campaign_id = data['pe_campaign_id']

        PeCampaign_obj = PeCampaign.objects.get(id=pe_campaign_id)

        user_survey_obj = UserSurvey.objects.all().values('id')

        print('links external-===>',PeCampaign_obj.external_profile_link)
        if (PeCampaign_obj.pe_campaign_type_id == int(1)):
            if PeCampaign_obj.internal_campaign_generated_link != "" and PeCampaign_obj.external_profile_link == "":
                for i in list(user_survey_obj):
                    # encrypted_uid = encrypt(str(i['id']),iv)
                    encoded_user_id = hashids.encode(int(i['id']))
                    offer_link = PeCampaign_obj.internal_campaign_generated_link+"&uid="+str(encoded_user_id)

                    if UserSurveyOffers.objects.filter(user_survey_id=i['id'], offer_link=offer_link, is_attened=False).exists():
                        pass
                    else:
                        UserSurveyOffers.objects.create(survey_name=PeCampaign_obj.campaign_name, points_for_survey=PeCampaign_obj.points, user_survey_id=i['id'], offer_link=offer_link)
            if PeCampaign_obj.external_profile_link != "" and PeCampaign_obj.internal_campaign_generated_link == "":
                # encrypted_uid = encrypt(str(i['id']),iv)
                encoded_user_id = hashids.encode(int(i['id']))
                offer_link = PeCampaign_obj.external_profile_link+"&uid="+str(encoded_user_id)

                if UserSurveyOffers.objects.filter(user_survey_id=i['id'], offer_link=offer_link, is_attened=False).exists():
                    pass
                else:
                    UserSurveyOffers.objects.create(survey_name=PeCampaign_obj.campaign_name, points_for_survey=PeCampaign_obj.points, user_survey_id=i['id'], offer_link=offer_link)
        else:
            print("not create")
          
        return Response({'message': "survey  assigned successfully"})

    def delete(self, request):
        UserSurveyOffers.objects.all().delete()
        return Response({'message': 'deleted'})

from hashids import Hashids
from comman.scheduler import *

# @method_decorator([authorization_required], name='dispatch')
class EmailSendOut(APIView):
    def post(self, request):
        data = request.data 

        hashids = Hashids(min_length=8)

        template_id = data.get('template_id')
        shedule = data['shedule']
        emails = data['emails']
        pe_campaign_id = data['pe_campaign_id']

        val = EmailTemplate.objects.get(id=template_id)
        
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

        # print("emails==>>>ksalkd==>>",UserSurvey.objects.filter(email__in=emails).values('id'))



        if shedule is None:
            for i in emails:
                panelist_obj = UserSurvey.objects.get(email=i)
                panelist_id = panelist_obj.id

                panelist_first_name.string.replace_with(panelist_obj.first_name)
                panelist_last_name.string.replace_with(panelist_obj.last_name)
                # surveyTime.string.replace_with(PeCampaign.objects.filter(id=pe_campaign_id).last().actual_survey_length)
                points.string.replace_with(PeCampaign.objects.filter(id=pe_campaign_id).last().points)

                # encrypted_uid = encrypt(str(panelist_id),iv)
                encoded_user_id = hashids.encode(int(panelist_id))

                print("panelist id",panelist_id, PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link)
                clss['href'] = PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link+"&uid="+str(encoded_user_id)

                clss_link_val.append(PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link+"&uid=<#user_id#>")

                em_body = soup.prettify()
                email = EmailMessage(subject, em_body, from_email=sender, to=[i])
                email.content_subtype = "html"
                email.send(fail_silently=False)  

                if UserSurveyOffers.objects.filter(user_survey_id=panelist_id, offer_link=PeCampaign.objects.get(id=pe_campaign_id).    internal_campaign_generated_link+"&uid="+str(encoded_user_id)).exists():
                    pass
                else:
                    UserSurveyOffers.objects.create(survey_name=PeCampaign.objects.get(id=pe_campaign_id).campaign_name, points_for_survey=PeCampaign.objects.get(id=pe_campaign_id).points ,user_survey_id=panelist_id, offer_link=PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link+"&uid="+str(encoded_user_id), survey_type=PeCampaign.objects.get(id=pe_campaign_id).pe_campaign_type)

            return Response({'result': {'count': 'mail has been sent to all the panelist email ids'}})
        else:
            
            date_string = 'Mon Feb 06 2023 16:38:21 GMT+0530 (India Standard Time)'.replace('(India Standard Time)', '').rstrip()
            datetime_object = datetime.datetime.strptime(date_string, '%a %b %d %Y %H:%M:%S %Z%z').strftime("%Y-%m-%d %H:%M:%S")

            print("datetime_object==>", datetime_object)

            for i in emails:
                panelist_id = UserSurvey.objects.get(email=i).id

                encoded_user_id = hashids.encode(int(panelist_id))

                clss['href'] = PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link+"&uid="+str(encoded_user_id)
                clss_link_val.append(PeCampaign.objects.get(id=pe_campaign_id).internal_campaign_generated_link+"&uid=<#user_id#>")

                em_body = soup.prettify()
                # email = EmailMessage(subject, em_body, from_email=sender, to=[i])
                # email.content_subtype = "html"
                # email.send(fail_silently=False) 

                sheduleTask(datetime_object, subject, em_body, sender, i)
            # sheduleTask(datetime_object)
            return Response({'result': {'count': 'Job is scheduled'}})

from robas.encrdecrp import decrypt
import requests

# @method_decorator([authorization_required], name='dispatch')
class pecampaignMaskedLink(APIView):
    def get(self, request, pcid, uid):

        r = requests.get('https://prod.rtymgt.com/api/v4/respondents/search/5e53da50-a809-4dbc-aca8-89e47566041f?sn_ud=170716409&sy_nr=20210575&rt_cy_ce=us&rt_sr_pd='+str(uid))
        print("josn data=====>>",r.json())
        if r.json()['Surveys'][0]['duplicate_score'] == 100 and r.json()['Surveys'][0]['duplicate_potential'] == 'high':
            return HttpResponseRedirect(settings.LIVE_URL+"/survey-terminated")

        hashids = Hashids(min_length=8)
        ints = hashids.decode(str(uid))
        descrypted_uid = list(ints)[0]
        print(list(ints)[0])

        request.session['pe-campaign-offer-url'] = settings.LIVE_URL+"/pcid="+str(pcid)+"&uid="+str(uid)

        if PeCampaignSurvey.objects.filter(panelist_id=descrypted_uid, pecampaign_id=pcid).exists():
            return HttpResponseRedirect(settings.LIVE_URL+"/already-attended-survey")
        else:
            return redirect(settings.LIVE_URL+'/surveyTemplate?uid='+str(uid)+'&pcid='+str(pcid))

@method_decorator([authorization_required], name='dispatch')
class RedemptionView(GenericAPIView):
    def get(self, request, pk):
        if Redemption.objects.filter(id=pk).exists():
            val = Redemption.objects.get(id=pk)
            serializer =  RedemptionSerializer(val)

            urls = str(Redemption.objects.get(id=pk).image)
            
            image_url = settings.LIVE_URL+'/media'+urls
            img_base64 = base64.b64encode(requests.get(image_url).content)


            updated_data = serializer.data

            updated_data['base64Image'] = img_base64

            return Response({'result': {'redemption': updated_data}})
        return Response({'result': {'error': 'no redemption found'}}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data

        market = data['market']
        name = data['name']
        threshold_value = data['threshold_value']
        description = data['description']
        image = data['image']
        is_instant_redemption = data['is_instant_redemption']
        is_edenred_redemption = data['is_edenred_redemption']    

        split_base_url_data = image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = "/instantInsight/site/public/media/redemption_images/"+name+'.png'
        fname1 = '/redemption_images/'+name+'.png'
        ss=  open(filename1, 'wb')
        print(ss)
        ss.write(imgdata1)
        ss.close()   

        if Redemption.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(market) > 1:
            redmption_obj = Redemption.objects.create(market = 'Multiple' ,name = name ,threshold_value = threshold_value ,description = description ,image = fname1 ,is_instant_redemption = is_instant_redemption ,is_edenred_redemption = is_edenred_redemption)
        else:
            redmption_obj = Redemption.objects.create(market = 'Single' ,name = name ,threshold_value = threshold_value ,description = description ,image = fname1 ,is_instant_redemption = is_instant_redemption ,is_edenred_redemption = is_edenred_redemption)

        for i in market:
            MarketWiseRedemption.objects.create(redemption_id=redmption_obj.id, market_id=i['id'])
        return Response({'result': {'redemption': 'redemption created successfully'}})

    def put(self, request, pk):
        data = request.data

        market = data['market']
        name = data['name']
        threshold_value = data['threshold_value']
        description = data['description']
        image = data['image']
        is_instant_redemption = data['is_instant_redemption']
        is_edenred_redemption = data['is_edenred_redemption']

        split_base_url_data = image.split(';base64,')[1]
        imgdata1 = base64.b64decode(split_base_url_data)
        filename1 = "/instantInsight/site/public/media/redemption_images/"+name+'.png'
        fname1 = '/redemption_images/'+name+'.png'
        ss=  open(filename1, 'wb')
        print(ss)
        ss.write(imgdata1)
        ss.close()   

        if Redemption.objects.filter(id=pk).exists():
            if len(market) > 1:
                redmption_obj = Redemption.objects.filter(id=pk).update(market = 'Multiple' ,name = name ,threshold_value = threshold_value ,description = description ,image = fname1 ,is_instant_redemption = is_instant_redemption ,is_edenred_redemption = is_edenred_redemption)
            else:
                redmption_obj = Redemption.objects.filter(id=pk).update(market = 'Single' ,name = name ,threshold_value = threshold_value ,description = description ,image = fname1 ,is_instant_redemption = is_instant_redemption ,is_edenred_redemption = is_edenred_redemption)
            return Response({'result': {'redemption':'redemption updated Successfully'}})
        return Response({'result': {'error':'no data found to update'}}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk):
        if Redemption.objects.filter(id=pk).exists():
            Redemption.objects.filter(id=pk).delete()
            return Response({'result': {'redemption':'redemption deleted successfully'}})
        return Response({'result': {'redemption':'no data found to delete'}}, status=status.HTTP_404_NOT_FOUND)  

@method_decorator([authorization_required], name='dispatch')
class UploadRedemption(APIView):
    def post(self, request):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return Response({'Result': {'Error': 'File Format should be csv'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        dataset = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(dataset)
        next(io_string)
        
        res = {'redemption_id': '', 'user_survey_id': '', 'date_of_redemption': '',  'redemption_value': '', 'redemption_status': '', 'ps_catelog_id': '',  'redeem_choice': '', 'country': '', 'source': '', 'membership_status': '', 'first_name': '', 'last_name': '', 'house_number': '', 'street': '', 'city': '', 'postal_code': '', 'state': '', 'mobile_number': '', 'earned_points': '', 'spent_points': '', 'points': '', 'voucher_code': '', 'pin': '', 'amount': '', 'expiry_date': '', 'paypal_id': '', 'paytm_id': '', 'redemption_source': ''}
        for col in csv.reader(io_string):
            # print(col)
            res['redemption_id'] =col[0]
            res['user_survey_id'] =col[1]
            res['date_of_redemption'] =col[2]
            res['redemption_value'] =col[3]
            res['redemption_status'] =col[4]
            res['ps_catelog_id'] =col[5]            
            res['redeem_choice'] =col[6]
            res['country'] =col[7]
            res['source'] =col[8]
            res['membership_status'] =col[9]
            res['first_name'] =col[10]
            res['last_name'] =col[11]
            res['house_number'] =col[12]
            res['street'] =col[3]
            res['city'] =col[14]
            res['postal_code'] =col[15]
            res['state'] =col[16]
            res['mobile_number'] =col[17]
            res['earned_points'] =col[18]
            res['spent_points'] =col[19]
            res['points'] =col[20]
            res['voucher_code'] =col[21]
            res['pin'] =col[22]
            res['amount'] =col[23]
            res['expiry_date'] =col[24]
            res['paypal_id'] =col[25]
            res['paytm_id'] =col[26]
            res['redemption_source'] =col[27]

            size = len(res['date_of_redemption'])
            mod_string = res['date_of_redemption'][:size - 13]
            converted_time = time.mktime(datetime.datetime.strptime(mod_string, "%d %b %Y").timetuple())

            data = PanelistIncentive.objects.create(redemption_id=res['redemption_id'], user_survey_id=res['user_survey_id'], date_of_redemption=res['date_of_redemption'], redemption_value=res['redemption_value'], redemption_status=res['redemption_status'], ps_catelog_id=res['ps_catelog_id'], redeem_choice=res['redeem_choice'], country=res['country'], source=res['source'], membership_status=res['membership_status'], first_name=res['first_name'], last_name=res['last_name'], house_number=res['house_number'], street=res['street'], city=res['city'], postal_code=res['postal_code'], state=res['state'], mobile_number=res['mobile_number'], earned_points=res['earned_points'], spent_points=res['spent_points'], points=res['points'], voucher_code=res['voucher_code'], pin=res['pin'], amount=res['amount'], expiry_date=res['expiry_date'], paypal_id=res['paypal_id'], paytm_id=res['paytm_id'],  redemption_source=res['redemption_source'], timestamp_date=converted_time)

        return Response({'result': {'message': 'redemption uploaded successfully'}})

@method_decorator([authorization_required], name='dispatch')
class DownloadRedemptionList(APIView):
    def post(self, request):

        data = request.data

        date_from = data['date_from']
        date_to = data['date_to']

        converted_time_from = time.mktime(datetime.datetime.strptime(date_from, "%d %b %Y").timetuple())
        converted_time_to = time.mktime(datetime.datetime.strptime(date_to, "%d %b %Y").timetuple())

        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)

        writer.writerow(['redemption_id', 'user_survey_id', 'date_of_redemption', 'redemption_value', 'redemption_status' ,'ps_catelog_id', 'redeem_choice' ,'country' ,'source' ,'membership_status' ,'first_name' ,'last_name' ,'house_number' ,'street' ,'city' ,'postal_code' ,'state' ,'mobile_number' ,'earned_points' ,'spent_points' ,'points' ,'voucher_code' ,'pin' ,'amount' ,'expiry_date' ,'paypal_id' ,'paytm_id' ,'redemption_source'])

        for i in PanelistIncentive.objects.filter(timestamp_date__range=(converted_time_from, converted_time_to)).values_list('redemption_id', 'user_survey_id', 'date_of_redemption', 'redemption_value', 'redemption_status' ,'ps_catelog_id', 'redeem_choice' ,'country' ,'source' ,'membership_status' ,'first_name' ,'last_name' ,'house_number' ,'street' ,'city' ,'postal_code' ,'state' ,'mobile_number' ,'earned_points' ,'spent_points' ,'points' ,'voucher_code' ,'pin' ,'amount' ,'expiry_date' ,'paypal_id' ,'paytm_id' ,'redemption_source'):
            
            writer.writerow(i)

        response['Content-Disposition'] = 'attachment; filename="pecampaign.csv"'

        return response

# class PeCampaignPageApiView(GenericAPIView):
#     def get(self, request): 
#         p_campaign_id = request.query_params['pe_campaign_id']

#         get_page_id = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(Q(pe_campaign_id=p_campaign_id)).values_list('page_id', flat=True).distinct()
#         print("get+page_id", get_page_id)
        
#         data = []

#         for i in get_page_id:
#             # print("i",i)
#             quest_id = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(Q(page_id=i)).values('question_library_id')
#             get_data_question = QuestionLibrary.objects.filter(id__in=quest_id).values()
#             for j in get_data_question:
#                 question_type = QuestionType.objects.get(id=j.get('question_type_id'))
#                 print("qt",question_type)
#                 question_category = QuestionCategory.objects.get(id=j.get('question_category_id'))
#                 quest_type={}

#                 quest_type = {
#                     'question_type': question_type.name,
#                     'question_category': question_category.name
#                 }

#             page_data = Page.objects.get(id=i)
#             dict = {
#                 'page_id':page_data.id,
#                 'page_name':page_data.name,
#                 'question_data':get_data_question,
#                 'question_details': quest_type
#             }
#             data.append(dict)

#         return Response({'result': data})

@method_decorator([authorization_required], name='dispatch')
class PeCampaignPageApiView(GenericAPIView):
    def get(self, request): 
        pe_campaign_id = request.query_params['pe_campaign_id']

        if Page.objects.filter(pe_campaign_id=pe_campaign_id).exists():
            final_output = Page.objects.filter(pe_campaign_id=pe_campaign_id).values()
            print(final_output)

        # print("quryparms===",p_campaign_id)

        # if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=p_campaign_id).exists():
        #     res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=p_campaign_id).values()
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
                    

            # print(final_output)
            return Response({'result': final_output})
        return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)

# class PeCampaignPageApiView(GenericAPIView):
#     def get(self, request): 
#         p_campaign_id = request.query_params['pe_campaign_id']
#         print("quryparms===",p_campaign_id)

#         if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=p_campaign_id).exists():
#             res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=p_campaign_id).values()
#             # print(res)
#             final_output = []
#             page_id = []


#             json_data = {'page_id': '','page_name': '', 'questions':{'question_id': '','question_text': '', 'question_category': '', 'question_type': ''}}
#             for i in res:
#                 print("res==",i)
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
                    

#             # print(final_output)
#             return Response({'result': final_output})
#         return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class RearrangeQuestionPosition(APIView):
    def post(self, request):
        data = request.data

        QuestionLibrary.objects.filter(id=data['question_id']).update(position_value=data['postion_value'])
        return Response({'message': 'questions rearranged successfully'})

@method_decorator([authorization_required], name='dispatch')
class PageApiview(GenericAPIView):
    def get(self, request,pk):
        final_result = []
        questions = {}
        res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=pk).values(
            'question_library_id',
            'question_library__question_name',
            'question_library__question_type_id',
            'question_library__question_category_id',
            'question_library__question_type__name',
            'question_library__question_category__name',
            'question_library__position_value',
        )
        for j in res:
            questions['questions_id'] = j['question_library_id']
            questions['question_name'] = j['question_library__question_name']
            questions['question_type_id'] = j['question_library__question_type_id']
            questions['question_type'] = j['question_library__question_type__name']
            questions['question_category'] = j['question_library__question_category__name']
            questions['question_category_id'] = j['question_library__question_category_id']
            questions['position_value'] = j['question_library__position_value']
            questions['page_id'] = pk

            questions['language_of_questions'] = []
            language_question_dict = {}
            language_data = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=j['question_library_id']).values(
                'id',
                'base_queestion_id',
                'created_question_language__language',
                'created_question_language__question_name',
                'created_question_language__id',
                'created_question_language__question_type__name',
                'created_question_language__question_type__id',
                'created_question_language__question_category__name',
                'created_question_language__question_category__id',
            )

            for k in language_data:
                questions['language_of_questions'].append(k)

            final_result.append(questions)
            questions = {}
        return Response({'result': {'question_data': final_result}})


        # print(res)
        # qst = []
        # for i in res:
        #    qst.append(i['question_library_id']) 

        # data = QuestionLibrary.objects.filter(id__in=qst).values()
        # # print("data",data)
        # for j in data:
        #     questions['questions_id'] = j['id']
        #     questions['question_name'] = j['question_name']
        #     question_type = QuestionType.objects.get(id=j['question_type_id'])
        #     question_category = QuestionCategory.objects.get(id=j['question_category_id'])
        #     questions['question_type_id'] = j['question_type_id']
        #     questions['question_type'] = question_type.name
        #     questions['question_category'] = question_category.name
        #     questions['question_category_id'] = j['question_category_id']
        #     questions['position_value'] = j['position_value']
        #     questions['page_id'] = pk

        #     questions['language_of_questions'] = []
        #     language_question_dict = {}
        #     language_data = QuestionLibraryWithLanguages.objects.filter(base_queestion_id=j['id']).values(
        #         'id',
        #         'base_queestion_id',
        #         'created_question_language__language',
        #         'created_question_language__question_name',
        #         'created_question_language__id',
        #         'created_question_language__question_type__name',
        #         'created_question_language__question_type__id',
        #         'created_question_language__question_category__name',
        #         'created_question_language__question_category__id',
        #     )

        #     for k in language_data:
        #         questions['language_of_questions'].append(k)

        #     final_result.append(questions)
        #     questions = {}


        # =================================================================
        


    # def post(self, request):
    #     data = request.data

    #     name = data['name']
    #     pe_campaign_id = data['pe_campaign_id']
    #     campaign_id = data['campaign_id']
    #     prescreener_id = data['prescreener_id']
    #     # question_library_id = data['question_library_id']

    #     if pe_campaign_id is not None:
    #         if Page.objects.filter(Q(name=name)&Q(pe_campaign_id=pe_campaign_id)).exists():
    #             return Response({'error': {'message': 'name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

    #         res = Page.objects.create(name=name, pe_campaign_id=pe_campaign_id)

    #         if question_library_id is not None: 
    #             for questions in question_library_id:
    #                 if QuestionLibrary.objects.filter(id=questions).exists():
    #                     question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(pe_campaign_id=pe_campaign_id, question_library_id=questions, page_id=res.id)
    #                     print("=====",question_library.id)
    #                 else:
    #                     return Response({'error': {'message': 'question ids not found'}})
    #         else:
    #             PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, page_id=res.id)

    #     if campaign_id is not None:
    #         if Page.objects.filter(Q(name=name)&Q(campaign_id=campaign_id)).exists():
    #             return Response({'error': {'message': 'name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

    #         res = Page.objects.create(name=name, campaign_id=campaign_id)
    #         PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(campaign_id=campaign_id, page_id=res.id)

    #         if question_library_id is not None: 
    #             for questions in question_library_id:
    #                 if QuestionLibrary.objects.filter(id=questions).exists():
    #                     question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(campaign_id=campaign_id, question_library_id=questions, page_id=res.id)
    #                     print("=====",question_library.id)
    #                 else:
    #                     return Response({'error': {'message': 'question ids not found'}})
    #         else:
    #             PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, page_id=res.id)

    #     if prescreener_id is not None:
    #         if Page.objects.filter(Q(name=name)&Q(prescreener_id=prescreener_id)).exists():
    #             return Response({'error': {'message': 'name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

    #         res = Page.objects.create(name=name, prescreener_id=prescreener_id)

    #         if question_library_id is not None: 
    #             for questions in question_library_id:
    #                 if QuestionLibrary.objects.filter(id=questions).exists():
    #                     question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, question_library_id=questions, page_id=res.id)
    #                     print("=====",question_library.id)
    #                 else:
    #                     return Response({'error': {'message': 'question ids not found'}})
    #         else:
    #             PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, page_id=res.id)

    #     return Response({'result':{'message': 'page created successfully'}})

    def post(self, request):
        data = request.data

        page_id = data['page_id']
        pe_campaign_id = data['pe_campaign_id']
        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']
        question_library_id = data['question_library_id']

        if pe_campaign_id is not None:
            if question_library_id is not None: 
                for questions in question_library_id:
                    if QuestionLibrary.objects.filter(id=questions).exists():
                        if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=pe_campaign_id, question_library_id=questions, page_id=page_id).exists():
                            return Response({'message': 'Question already exist for this page'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(pe_campaign_id=pe_campaign_id, question_library_id=questions, page_id=page_id)
                            print("=====",question_library.id)
                    else:
                        return Response({'error': {'message': 'question ids not found'}})
            else:
                PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(pe_campaign_id=pe_campaign_id, page_id=page_id)

        if campaign_id is not None:
            if question_library_id is not None: 
                for questions in question_library_id:
                    if QuestionLibrary.objects.filter(id=questions).exists():
                        if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(campaign_id=campaign_id,question_library_id=questions, page_id=page_id).exists():
                            return Response({'message': 'Question already exist for this page'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(campaign_id=campaign_id, question_library_id=questions, page_id=page_id)
                            print("=====",question_library.id)
                    else:
                        return Response({'error': {'message': 'question ids not found'}})
            else:
                PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(campaign_id=campaign_id, page_id=page_id)

        if prescreener_id is not None:
            if question_library_id is not None: 
                for questions in question_library_id:
                    if QuestionLibrary.objects.filter(id=questions).exists():
                        if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id, question_library_id=questions, page_id=page_id).exists():
                            return Response({'message': 'Question already exist for this page'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                        else:
                            question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, question_library_id=questions, page_id=page_id)
                        print("=====",question_library.id)
                    else:
                        return Response({'error': {'message': 'question ids not found'}})
            else:
                PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, page_id=page_id)

        return Response({'result':{'message': 'page question created successfully'}})

    def put(self, request, pk):
        data = request.data

        pe_campaign_id = data['pe_campaign_id']
        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']
        question_library_id = data['question_library_id']

        if pe_campaign_id is not None:
            if Page.objects.filter(Q(name=name)&Q(pe_campaign_id=pe_campaign_id)).exists():
                res = Page.objects.filter(id=pk).update(name=name, pe_campaign_id=pe_campaign_id)
            else:
                res = Page.objects.create(name=name, pe_campaign_id=pe_campaign_id)
            
            if question_library_id is not None: 
                for questions in question_library_id:
                    if QuestionLibrary.objects.filter(id=questions).exists():
                        question_library = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(pe_campaign_id=pe_campaign_id, question_library_id=questions, page_id=res.id)
                        print("=====",question_library.id)
                    else:
                        return Response({'error': {'message': 'question ids not found'}}, status=HTTP_404_NOT_FOUND)
            else:
                PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=prescreener_id, page_id=res.id)

        return Response({'result': "page updated successfully"})

    def delete(self, request, pk):
        if Page.objects.filter(id=pk).exists():
            Page.objects.filter(id=pk).delete()
            return Response({'message': 'page deleted successfully!'})

@method_decorator([authorization_required], name='dispatch')
class CreatPage(APIView):
    def post(self, request):
        data = request.data

        name = data['name']
        pe_campaign_id = data['pe_campaign_id']
        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']

        if campaign_id is not None:
            if Page.objects.filter(Q(name=name)&Q(campaign_id=campaign_id)).exists():
                return Response({'error': {'message': 'Page name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                res = Page.objects.create(name=name, campaign_id=campaign_id)

        if pe_campaign_id is not None:
            if Page.objects.filter(Q(name=name)&Q(pe_campaign_id=pe_campaign_id)).exists():
                return Response({'error': {'message': 'Page name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                res = Page.objects.create(name=name, pe_campaign_id=pe_campaign_id)

        if prescreener_id is not None:
            if Page.objects.filter(Q(name=name)&Q(prescreener_id=prescreener_id)).exists():
                return Response({'error': {'message': 'Page name aleady exist'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                res = Page.objects.create(name=name, prescreener_id=prescreener_id)
        
        return Response({'error': {'message': 'page created'}})

@method_decorator([authorization_required], name='dispatch')
class PageRoutingLogicApiView(GenericAPIView):
    def get(self, request):
        
        # if request.query_params['campaign_id'] != "null":
        if request.GET.get('campaign_id'):
            data = PageRoutingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')
        
        # if request.query_params['prescreener_id'] != "null":
        if request.GET.get('prescreener_id'):
            data = PageRoutingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id']).values()

            for i in data:
                for j in i['logic']['dataset']:
                    option_name = QuestionChoice.objects.get(id=j['answer']).name
                    question_name = QuestionLibrary.objects.get(id=j['question_id']).question_name
                    operator_name = QuestionOperator.objects.get(id=j['operator_id']).name

                    j['answer_name'] = option_name
                    j['question_name'] = question_name
                    j['operator_name'] = operator_name


                    
                    # QuestionLibrary
                    # QuestionChoice
                    # QuestionOperator
            return Response({'data': data})

        if request.query_params['routing_logic_id'] != "null":
            # return Response('page_id')
            data = PageRoutingLogic.objects.filter(id=request.query_params['routing_logic_id']).values()
            return Response({'data': data})

        return Response('nothing id')

    def post(self, request):
        data=request.data

        name = data['name']
        page_id = data['page_id']
        logic = data['logic']
        targeted_page = data['targeted_page']
        targeted_page_name = data['targeted_page_name']

        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']
        pe_campaign_id = data['pe_campaign_id']

        if Page.objects.filter(id=page_id).exists():
            res = PageRoutingLogic.objects.create(name=name, page_id=page_id, logic=logic, targeted_page=targeted_page, targeted_page_name=targeted_page_name, pe_campaign_id=pe_campaign_id ,campaign_id=campaign_id,prescreener_id=prescreener_id)
            return Response({'result':{'message': 'routing logic created successfully'}})
        return Response({'error': {'message': 'page id does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        routing_logic_id = request.GET.get('routing_logic_id')

        if request.GET.get('campaign_id'):
            data = PageRoutingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')

        if request.GET.get('prescreener_id'):
            data = PageRoutingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id'], id=routing_logic_id).delete()
            return Response({'data': "routing logic deleted successfully!"})

        return Response("no") 



@method_decorator([authorization_required], name='dispatch')
class PageMaskingLogicApiView(GenericAPIView):    
    def get(self, request):
        
        # if request.query_params['campaign_id'] != "null":
        if request.GET.get('campaign_id'):
            data = PageRoutingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')
        
        # if request.query_params['prescreener_id'] != "null":
        if request.GET.get('prescreener_id'):
            data = PageMaskingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id']).values()

            for j in data:
                option_name = QuestionChoice.objects.get(id=j['questio_choice_id']).name
                question_name = QuestionLibrary.objects.get(id=j['question_id']).question_name

                hide_answer_name = QuestionChoice.objects.get(id=j['hide_answer_id']).name
                targeted_question = QuestionLibrary.objects.get(id=j['target_question_id']).question_name

                j['answer_name'] = option_name
                j['targeted_question_name'] = targeted_question
                j['hide_answer_name'] = hide_answer_name
                j['question_name'] = question_name
            return Response({'data': data})

        if request.query_params['routing_logic_id'] != "null":
            # return Response('page_id')
            data = PageRoutingLogic.objects.filter(id=request.query_params['routing_logic_id']).values()
            return Response({'data': data})

        return Response('nothing id')

    def post(self, request):
        data = request.data
        print(data)

        name = data['name']
        page_id = data['page_id']
        question_id = data['question_id']
        questio_choice_id = data['questio_choice_id']
        target_question_id = data['target_question_id']
        hide_answer_id = data['hide_answer_id']

        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']
        pe_campaign_id = data['pe_campaign_id']

        if Page.objects.filter(id=page_id).exists():
            res = PageMaskingLogic.objects.create(name=name ,page_id=page_id ,question_id=question_id ,questio_choice_id=questio_choice_id ,target_question_id=target_question_id ,hide_answer_id=hide_answer_id , pe_campaign_id=pe_campaign_id ,campaign_id=campaign_id,prescreener_id=prescreener_id)
            return Response({'result':{'message': 'masking logic created successfully'}})
        return Response({'error': {'message': 'page id does not exist'}}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        masking_logic_id = request.GET.get('masking_logic_id')

        if request.GET.get('campaign_id'):
            data = PageMaskingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')

        if request.GET.get('prescreener_id'):
            data = PageMaskingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id'], id=masking_logic_id).delete()
            return Response({'data': "masking logic deleted successfully!"})

        return Response("no") 

@method_decorator([authorization_required], name='dispatch')
class PagePipingLogicApiView(GenericAPIView):  
    def get(self, request):
        
        # if request.query_params['campaign_id'] != "null":
        if request.GET.get('campaign_id'):
            data = PageRoutingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')
        
        # if request.query_params['prescreener_id'] != "null":
        if request.GET.get('prescreener_id'):
            data = PagePipingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id']).values()

            for j in data:
                question_name = QuestionLibrary.objects.get(id=j['question_id']).question_name
                j['question_name'] = question_name
            return Response({'data': data})

        if request.query_params['routing_logic_id'] != "null":
            # return Response('page_id')
            data = PageRoutingLogic.objects.filter(id=request.query_params['routing_logic_id']).values()
            return Response({'data': data})

        return Response('nothing id')

    def post(self, request):
        data = request.data

        name= data['name']
        page_id= data['page_id']
        question_id= data['question_id']
        next_question_id= data['next_question_id']
        piped_question_text= data['piped_question_text']

        campaign_id = data['campaign_id']
        prescreener_id = data['prescreener_id']
        pe_campaign_id = data['pe_campaign_id']

        if Page.objects.filter(id=page_id).exists():
            res = PagePipingLogic.objects.create(name=name, page_id=page_id, question_id=question_id, next_question_id=next_question_id, next_question_text=piped_question_text, pe_campaign_id=pe_campaign_id ,campaign_id=campaign_id,prescreener_id=prescreener_id)
            return Response({'result':{'message': 'piping logic created successfully'}})
        return Response({'error': {'message': 'page id does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        piping_logic_id = request.GET.get('piping_logic_id')

        if request.GET.get('campaign_id'):
            data = PagePipingLogic.objects.filter(campaign_id=request.query_params['campaign_id']).values()
            return Response({'data': data})

        # if request.query_params['pe_campaign_id'] != "null":
        if request.GET.get('pe_campaign_id'):
            return Response('pe_campaign id')

        if request.GET.get('prescreener_id'):
            data = PagePipingLogic.objects.filter(prescreener_id=request.query_params['prescreener_id'], id=piping_logic_id).delete()
            return Response({'data': "piping logic deleted successfully!"})

        return Response("no")  


@method_decorator([authorization_required], name='dispatch')
class PeCampaignRoutingLogicQuestions(GenericAPIView):
    def get(self, request, pk, p_id):  #send pe-campaign_id in id and page_id in pk

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

        all_pages_for_campaign = Page.objects.filter(pe_campaign_id=p_id).values()
        for pges in all_pages_for_campaign:
            print(pges['name'])
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

        exclude_page = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.exclude(page_id=pk).values() & PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(pe_campaign_id=p_id).values()
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
        
        return Response({'questions': val, 'targeted_page': val2})   

@method_decorator([authorization_required], name='dispatch')
class QuestionChoiceForQuestion(GenericAPIView):
    def get(self, request, pk, p_id): #send question_id

        if QuestionLibrary.objects.filter(id=pk).exists():
            qst = QuestionLibrary.objects.get(id=pk)
            # print(qst.question_type_id)

            qst_choice = QuestionChoice.objects.filter(question_library_id=pk).values()

            answrs = []
            all_choice = {}
            for i in qst_choice:
                all_choice = {}
                all_choice['choice_id'] = i['id']
                all_choice['name'] = i['name']

                answrs.append(all_choice)

            question_type = QuestionType.objects.get(id=qst.question_type_id)
            print(question_type.name)

            val = questionType(self ,question_type.name)
            # print(val)

            print(qst.id)
            page_data = []
            p_data = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.exclude(question_library_id=qst.id).values() & PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=p_id).values()

            for x in p_data:
                # print(x)
                page_data.append(x['question_library_id'])

            print("===",page_data)

            val2 =[]
            qs = {}
            qst_data =QuestionLibrary.objects.filter(id__in=page_data).values()
            for y in qst_data:
                # print(y)
                qs['question_text'] = y['question_name']
                qs['question_id'] = y['id']
                val2.append(qs)
                qs={}
        
            return Response({'operators': val, 'answers': answrs, 'targeted_question': val2})
        return Response({'eror':'question id not found'}, status=HTTP_404_NOT_FOUND)
        # qst_choice = QuestionChoice.objects.filter(question_library_id=pk).values()
        # val = []
        # question_choice = {}
        # for j in qst_choice:
        #     print(j)
        #     question_choice['choice_id'] = j['id']
        #     question_choice['answers'] = j['text']
        #     val.append(question_choice)
        #     question_choice = {}
    
        # return Response({'choices': val})



  



        




