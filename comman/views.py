from django.shortcuts import render
from .models import *
from rest_framework.views import *
import googletrans
from googletrans import Translator
import itertools
from projects.models import *
from panelbuilding.models import *
from panelengagement.models import *
import datetime
from django.db.models import Q
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.utils.decorators import method_decorator
from account.backends_ import *
import pandas as pd

# Create your views here.
data = [
            {
                'month':1,
                'count': 0
            },
            {
                'month':2,
                'count': 0
            },
            {
                'month':3,
                'count': 0
            },
            {
                'month':4,
                'count': 0
            },
            {
                'month':5,
                'count': 0 
            },
            {
                'month':6,
                'count': 0
            },
            {
                'month':7,
                'count': 0
            },
            {
                'month': 8, 
                'count': 0
            },
            {
                'month':9,
                'count': 0
            },
            {
                'month':10,
                'count': 0
            },
            {
                'month':11,
                'count': 0
            },
            {
                'month':12,
                'count': 0
            }
]
x = [{'month': 8, 'count': 1}]



@method_decorator([authorization_required], name='dispatch')
class GlobalDashboard(APIView):
    def get(self, request):
        finalDict = {}

        finalDict['total_projects_created'] = Project.objects.all().count()
        finalDict['total_campaign_created'] = Campaign.objects.all().count()
        finalDict['total_pecampaign_created'] = PeCampaign.objects.all().count()
        finalDict['total_redemption_created'] = Redemption.objects.all().count()

        return Response({'data': [finalDict]})

    def post(self, request):
        data =  request.data
        year = data['year']
        project_list = [
            {
                'month':1,
                'count': 0
            },
            {
                'month':2,
                'count': 0
            },
            {
                'month':3,
                'count': 0
            },
            {
                'month':4,
                'count': 0
            },
            {
                'month':5,
                'count': 0 
            },
            {
                'month':6,
                'count': 0
            },
            {
                'month':7,
                'count': 0
            },
            {
                'month': 8, 
                'count': 0
            },
            {
                'month':9,
                'count': 0
            },
            {
                'month':10,
                'count': 0
            },
            {
                'month':11,
                'count': 0
            },
            {
                'month':12,
                'count': 0
            }
        ]

        campaign_list = [
            {
                'month':1,
                'count': 0
            },
            {
                'month':2,
                'count': 0
            },
            {
                'month':3,
                'count': 0
            },
            {
                'month':4,
                'count': 0
            },
            {
                'month':5,
                'count': 0 
            },
            {
                'month':6,
                'count': 0
            },
            {
                'month':7,
                'count': 0
            },
            {
                'month': 8, 
                'count': 0
            },
            {
                'month':9,
                'count': 0
            },
            {
                'month':10,
                'count': 0
            },
            {
                'month':11,
                'count': 0
            },
            {
                'month':12,
                'count': 0
            }
        ]

        pe_campaign_list = [
            {
                'month':1,
                'count': 0
            },
            {
                'month':2,
                'count': 0
            },
            {
                'month':3,
                'count': 0
            },
            {
                'month':4,
                'count': 0
            },
            {
                'month':5,
                'count': 0 
            },
            {
                'month':6,
                'count': 0
            },
            {
                'month':7,
                'count': 0
            },
            {
                'month': 8, 
                'count': 0
            },
            {
                'month':9,
                'count': 0
            },
            {
                'month':10,
                'count': 0
            },
            {
                'month':11,
                'count': 0
            },
            {
                'month':12,
                'count': 0
            }
        ]

        # start_month = request.data['start_month']

        # print(Project.objects.dates('created_date', 'month'))
        
        Project_obj = Project.objects.filter(start_date__year=year).annotate(month=ExtractMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')
        for i in list(Project_obj):
            print("i==", i)
            index = next((index for (index, d) in enumerate(project_list) if d["month"] == i['month']), None)
            print("==>>",i, index)
            project_list[index] = i

        campaign_obj = Campaign.objects.filter(start_date__year=year).annotate(month=ExtractMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')
        for i in list(campaign_obj):
            index = next((index for (index, d) in enumerate(campaign_list) if d["month"] == i['month']), None)
            campaign_list[index] = i

        pecampaign_obj = PeCampaign.objects.filter(created_date__year=year).annotate(month=ExtractMonth('created_date')).values('month').annotate(count=Count('id')).order_by('month')
        for i in list(pecampaign_obj):
            index = next((index for (index, d) in enumerate(pe_campaign_list) if d["month"] == i['month']), None)
            pe_campaign_list[index] = i
            

        return Response({
            "project": project_list,
            "campaign": campaign_list,
            "pe_campaign": pe_campaign_list
        })

@method_decorator(authorization_required, name='dispatch')
class DashboardAPi(APIView):
    def get(self, request):
        dashboard_obj = DashboardData.objects.all().values()
        return Response({'dashboard_data': dashboard_obj})


class Translatelanguage(APIView):
    def get(self, request):
        translator = Translator()

        templList = []
        tempDict = {}
        for k, l in itertools.zip_longest(googletrans.LANGUAGES.keys(), googletrans.LANGUAGES.values()):
            tempDict['code'] = k
            tempDict['langlauge'] = l
            templList.append(tempDict)
            tempDict = {}
        return Response({'data': templList})

    def post(self, request):
        data = request.data
        text = data['text']
        dest = data['dest']

        translator = Translator()
        data = translator.detect("Hello")
        print(data.lang)

        alldata = []
        converted_questions = {}

        for i in text:
            detetctes_lang = translator.detect(i['question_name'])
            # print("qust==>>",translator.translate(i['question_name'], src="en", dest=dest))
            converted_questions['question_name'] = translator.translate(i['question_name'], src=detetctes_lang.lang, dest=dest).text
            converted_questions['question_id'] = i['question_id']
            converted_questions['question_type'] = i['question_type']
            
            option_list = []
            option_text = {}
            for j in i['options']:
                detetctes_lang_opt = translator.detect(j['opt_text'])
                option_text['opt_id'] = j['opt_id']
                option_text['opt_text'] = translator.translate(j['opt_text'], src=detetctes_lang_opt.lang, dest=dest).text

                option_list.append(option_text)
                option_text = {}

            converted_questions['options'] = option_list 

            alldata.append(converted_questions)
            converted_questions = {}

        return Response({'text': alldata})


class UploadSupplierXLS(APIView):
    def post(self, request):
        supplier_excel_file = request.FILES['supplier_excel_file']

        if not supplier_excel_file.name.endswith('.xlsx'):
            return Response({'Result': {'Error': 'File Format should be xlsx'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        dataframe = pd.read_excel(supplier_excel_file)

        print("dataframe==>", dataframe)

        lit_of_supplier = [item for item in  dataframe['Vendor'].tolist()]
        print("lit_of_user_id==>",lit_of_supplier) 
        
        for i in lit_of_supplier:

            # Supplier.objects.create(Supplier_Name=i, is_for_project=True)
            Supplier.objects.filter(Supplier_Name=i).update(Status='Active')

        return Response({'message': 'file uploaded successfully'})


class AddEndPagesTemplate(APIView):
    def get(self, request):
        if request.query_params:
            template = CustomizeThankyouandTerminatePage.objects.filter(id=request.query_params['template_id']).values()
            return Response({'data': template})
        data = CustomizeThankyouandTerminatePage.objects.all().values()
        return Response({'data': data})

    def post(self, request):
        data = request.data

        page_id = data['page_id']

        if data['end_template_page_id']:
            page_obj = Page.objects.filter(id=page_id).update(end_template_page_id=data['end_template_page_id'])
        
        if data['html_code']:
            cus_pge_obj = CustomizeThankyouandTerminatePage.objects.create(inline_html_code=data['html_code'], name=data['name'])
            Page.objects.filter(id=page_id).update(end_template_page_id=cus_pge_obj.id)

        return Response({'message': 'templates uploaded successfully'})


    def put(self, request):
        data = request.data
        page_id = data['page_id']
        end_template_page_id = data['end_template_page_id']
        cus_pge_obj = CustomizeThankyouandTerminatePage.objects.filter(id=end_template_page_id).update(inline_html_code=data['html_code'], name=data['name'])
        Page.objects.filter(id=page_id).update(end_template_page_id=end_template_page_id)

        return Response({'message': 'template updated successfully'})

    def delete(self, request, page_id):
        # unlink template 

        data = request.data

        # page_id = data['page_id']
        Page.objects.filter(id=page_id).update(end_template_page_id=None)

        return Response({'message': 'template unlinked successfully'})


class SheduleTask(APIView):
    def get(self, request):
        pass




        