from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from usersurvey.serializers import *
from rest_framework.response import Response
from projects.models import *
from django.utils.decorators import method_decorator
from account.backends_ import *
from panelengagement.models import *
from prescreener.models import *
import datetime
from comman.models import *
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.auth.hashers import make_password


class PanelistForgotPasswordAPI(APIView):
    def post(self, request):
        data = request.data

        email = data['email']

        user_obj = UserSurvey.objects.get(email=email)

        full_name = user_obj.first_name + user_obj.last_name

        link = settings.LIVE_URL+"/panelist-reset-password/"+str(user_obj.id)
        html_path = 'panelist_forgot_password.html'
        context_data = {'link': link, 'name': full_name}
        email_html_template = get_template(html_path).render(context_data)
        receiver_email = email
        email_msg = EmailMessage('Forgot Password??', email_html_template, settings.APPLICATION_EMAIL, [receiver_email], reply_to=[settings.APPLICATION_EMAIL])

        email_msg.content_subtype='html'
        email_msg.send(fail_silently=False)

        return Response({'message': 'Mail has been sent to registered email successfully'})
        
# Create your views here.
# @method_decorator([authorization_required], name='dispatch')
class UserOffers(APIView): #user survey get all API
    def get(self, request):
        pe_campaign_name = request.query_params['pe_campaign_name']

        pe_campaign_id = PeCampaign.objects.get(campaign_name=pe_campaign_name).id

        page_obj = Page.objects.filter(pe_campaign_id=pe_campaign_id).values('id')
        # page_id = page_obj

        qst_data = []
        tempqust_details = {}
        quest_no = 1

        for i in page_obj:
            qst_lib = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=i['id']).values('question_library_id', 'question_library__question_name', 'question_library__question_type__name')
            for j in qst_lib:
                # print("qst data==>",j)
                tempqust_details['question_no'] = quest_no
                tempqust_details['question_id'] = j['question_library_id']
                tempqust_details['question_name'] = j['question_library__question_name']
                tempqust_details['question_type'] = j['question_library__question_type__name']
                # tempqust_details['question_choice'] = []

                options_obj = QuestionChoice.objects.filter(question_library_id=j['question_library_id']).values('id', 'name')
                tempqust_details['question_choice'] = options_obj

                qst_data.append(tempqust_details)
                tempqust_details = {}

                quest_no = quest_no + 1

        return Response({'pe_campaign_id': pe_campaign_id, 'qst_data': qst_data})

    def post(self, request):
        data = request.data
        user_offer = UserSurveyOffers.objects.filter(user_survey_id=data['panelist_id'])        
        serializer = userOfferSerializer(user_offer, many=True)
        serializer_type = list(serializer.data)
        
        return Response({'message': 'success', 'data': serializer.data})

# @method_decorator([authorization_required], name='dispatch')
class UserPoints(APIView):
    def post(self, request):
        data = request.data
        user_points = UserSurveyPoints.objects.filter(user_survey_id=data['panelist_id'])
        serializer = userPointsSerializer(user_points, many=True)
        return Response({'message': 'success', 'data': serializer.data})

# @method_decorator([authorization_required], name='dispatch')
class RedemeVocher(APIView):
    def get(self, request, user_id):

        print("request.user_agent.browser.family==>", request.user_agent.browser.family)

        user_survey_obj = UserSurvey.objects.get(id=user_id)

        market_wise_redemption = MarketWiseRedemption.objects.filter(market__name=user_survey_obj.country).values(
            'redemption_id',
            'redemption__name',
            'redemption__threshold_value',
            'redemption__image',
            'redemption__description'
        )

        earned_rewards = UserSurveyRewards.objects.filter(user_survey_id=user_id).values('earned_reward_id','earned_reward__name', 'earned_reward__threshold_value', 'earned_reward__description', 'earned_reward__image')
        
        return Response({'vovher': market_wise_redemption, 'earned_rewards': earned_rewards})

    def post(self, request):
        data = request.data
        
        # redemption_id = data['redemption_id'] audto generated id pk
        user_id = data['user_id']
        reward_value = data['reward_value']
        # redemption status will be open initially admin has to update after giving vocher to user 
        catelog_id = data['catelog_id'] # reward_id
        redeme_choice = data['redeme_choice'] #name of the vocher

        old_point_spent = UserSurveyPoints.objects.get(user_survey_id=int(user_id)).points_spent
        old_points_earned = UserSurveyPoints.objects.get(user_survey_id=int(user_id)).points_earned
        
        UserSurveyPoints.objects.filter(user_survey_id=int(user_id)).update(points_spent=(int(old_point_spent) + int(reward_value)))

        total_points_spent = UserSurveyPoints.objects.get(user_survey_id=int(user_id)).points_spent

        avaiable_points = int(UserSurveyPoints.objects.get(user_survey_id=int(user_id)).points_earned) - int(total_points_spent)

        total_available_points = UserSurveyPoints.objects.filter(user_survey_id=int(user_id)).update(available_points=avaiable_points)

        now = datetime.datetime.now()
        panelIncetive_obj = PanelistIncentive.objects.create(
            user_survey_id = user_id,
            date_of_redemption = datetime.datetime.now(),
            timestamp_date = datetime.datetime.timestamp(now),
            redemption_value = reward_value,
            redemption_status = "open",
            ps_catelog_id = catelog_id,
            redeem_choice = Redemption.objects.get(id=catelog_id).name,
            country = UserSurvey.objects.get(id=int(user_id)).country,
            first_name = UserSurvey.objects.get(id=int(user_id)).first_name,
            last_name = UserSurvey.objects.get(id=int(user_id)).last_name,
            city = UserSurvey.objects.get(id=int(user_id)).city,
            state = UserSurvey.objects.get(id=int(user_id)).state,
            earned_points = int(UserSurveyPoints.objects.get(user_survey_id=int(user_id)).points_earned),
            spent_points = reward_value,
            points = int(UserSurveyPoints.objects.get(user_survey_id=int(user_id)).available_points)
        )

        UserSurveyRewards.objects.create(user_survey_id=user_id, earned_reward_id=catelog_id)

        return Response({'message': 'points redeemed successfully'})

class ResetPanelistPassword(APIView):
    def post(self, request):
        data = request.data

        panelist_id = data['panelist_id']
        password = data['password']
        confirm_password = data['confirm_password']

        
        UserSurvey.objects.filter(id=panelist_id).update(password = make_password(password))

        return Response({'message': 'password updated successfully'})



