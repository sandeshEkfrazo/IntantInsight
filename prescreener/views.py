# from curses import panel
from operator import index
from re import A
from textwrap import indent
from unittest import skip
from django.shortcuts import render
from rest_framework import status
from prescreener.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from prescreener.serializers import *
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from comman.models import *
import io
import pandas as pd
import uuid
from django.utils.decorators import method_decorator
from account.backends_ import *
from projects.pagination import MyPagination
import random

# Create your views here.
@method_decorator([authorization_required], name='dispatch')
class AllQuestionlibrary(ListAPIView):
    serializer_class = QuestLibrarySerializer
    queryset = QuestionLibrary.objects.all()
    # pagination_class = MyPagination

@method_decorator([authorization_required], name='dispatch')
class QuestionTypes(ListAPIView):
    serializer_class = QuestionTypeSerializer
    queryset = QuestionType.objects.all()
    pagination_class = MyPagination
    # def get(self, request):
    #     values = QuestionType.objects.all().values()
    #     return Response({'result': {'question Type': values}})

    def post(self, request):
        data = request.data
        name = data['name']
        company = data['company']

        if QuestionType.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
        question_cat = QuestionType.objects.create(name=name, company=company)
        return Response({'result': {'queustion_type':'question type created successfully'}})

    def delete(self, request, pk):
        if QuestionType.objects.filter(id=pk).exists():
            QuestionType.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'queston type deleted successfully'}})
        return Response({'result': {'error': 'queston type id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

# @method_decorator([authorization_required], name='dispatch')
class QuestionCatagories(APIView):
    # serializer_class = QuestionCategorySerializer
    # queryset = QuestionCategory.objects.all()
    # pagination_class = MyPagination
    def get(self, request):
        values = QuestionCategory.objects.all().values()
        return Response({'results':  values})

    def post(self, request):
        data = request.data
        name = data['name']
        company = data['company']

        if QuestionCategory.objects.filter(name=name).exists():
            return Response({'Result': {'Error': 'Name Already Taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
        question_cat = QuestionCategory.objects.create(name=name, company=company)
        return Response({'result': {'queustion category':'question category created successfully'}})

    def delete(self, request, pk):
        if QuestionCategory.objects.filter(id=pk).exists():
            QuestionCategory.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'queston category deleted successfully'}})
        return Response({'result': {'error': 'queston category id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class Questionlibrary(GenericAPIView):
    def get(self, request, pk):
        if QuestionLibrary.objects.filter(id=pk).exists():
            value = QuestionLibrary.objects.filter(id=pk).values()
            return Response({'result': {'message': value}})
        return Response({'error': {'message': 'question not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request):
        prescreener_id = request.GET.get('prescreener_id')
        campaign_id = request.GET.get('campaign_id')
        pe_campaign_id = request.GET.get('pe_campaign_id')
        question_id = request.GET.get('question_id')
        page_id = request.GET.get('page_id')

        if campaign_id:
            value = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(question_library_id=question_id, campaign_id=campaign_id, page_id=page_id).delete()
            return Response({'result': {'message': "question deleted successfully"}})

        if pe_campaign_id:
            value = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(question_library_id=question_id, pe_campaign_id=pe_campaign_id, page_id=page_id).delete()
            return Response({'result': {'message': "question deleted successfully"}})

        if prescreener_id:
            # value = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(question_library_id=question_id, prescreener_id=prescreener_id, page_id=page_id).delete()
            value = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(question_library_id=question_id, prescreener_id=prescreener_id, page_id=page_id).update(is_deleted_question=True)
            return Response({'result': {'message': "question deleted successfully"}})

    def post(self, request):
        data = request.data
        language = data.get('language')
        question_name = data.get('question_name')
        question_text = data.get('question_text')
        instruction = data.get('instruction')

        question_type = data.get('question_type')
        question_cat = data.get('question_category')
        is_base_question = data['is_base_question']

        if QuestionLibrary.objects.filter(question_name=question_name, question_type_id=question_type, question_category_id=question_cat).exists():
            return Response({'message': 'Question Already Exist in the System'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        question = QuestionLibrary.objects.create(language=language, question_name=question_name, question_text=question_text, instruction=instruction, question_type_id=question_type, question_category_id=question_cat, is_base_question=is_base_question)
        
        if data['question_choice'] is not None:
         
            for values in data['question_choice']:
                value = QuestionChoice.objects.create(name=values['name'], text=values['text'], question_library_id=question.id)        

        return Response({'result': {'question_id': question.id}, 'message': 'question created successfully'})

@method_decorator([authorization_required], name='dispatch')
class DeleteQuestionFromQ_Lib(APIView):
    def delete(self,request, question_id):
        if QuestionLibrary.objects.filter(id=question_id).exists():
            QuestionLibrary.objects.filter(id=question_id).delete()
            return Response({'message': 'question deleted successfullt from Q-Lib'})
        return Response({'error': 'question not found with this id'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class QuestionLibraryWithLanguagesAPI(APIView):
    def get(self, request):
        return Response({'data': QuestionLibraryWithLanguages.objects.all().values(
            'id',
            'base_queestion__language',
            'base_queestion__question_name',
            'base_queestion__id',
            'base_queestion__question_type__name',
            'base_queestion__question_type__id',
            'base_queestion__question_category__name',
            'base_queestion__question_category__id',
        )})

    def post(self, request):
        data = request.data
        if QuestionLibrary.objects.filter(question_name=data['question_name']).exists():
            return Response({'error': "question with same name already exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            quest_obj = QuestionLibrary.objects.create(
                language = data['language'],
                question_name = data['question_name'],
                question_text = data['question_text'],
                instruction = data['instruction'],
                question_type_id = data['question_type'],
                question_category_id = data['question_category'],
                is_base_question=False
            )

            if data['question_choice'] is not None:
         
                for values in data['question_choice']:
                    value = QuestionChoice.objects.create(name=values['name'], text=values['text'], question_library_id=quest_obj.id) 

            QuestionLibraryWithLanguages.objects.create(base_queestion_id=data['base_question_id'], created_question_language_id=quest_obj.id)
            
            return Response({'message': 'question added successfully !'})

@method_decorator([authorization_required], name='dispatch')
class PrescreenerApiView(generics.ListCreateAPIView):
    serializer_class = PrescreenerQuestionLibrarySerializer
    queryset = PrescreenerQuestionLibrary.objects.all()
    pagination_class = MyPagination

    # def get(self, request):
    #     value = PrescreenerQuestionLibrary.objects.all().values()
    #     return Response({'Result': {'Prescreener': value}})

    def post(self, request):
        data = request.data
        name = data.get('name')
        link = data.get('link')
        enable_otp_verification = data.get('enable_otp_verification')
        project = data.get('project')
        question_library_id = data.get('question_library_id')

        r1 = random.randint(10, 100000)
        unique_id = str(r1)
        # generated_link = settings.LIVE_URL+"/#/prescreener_id="+str(unique_id)
        # generated_link = settings.LIVE_URL+"/prescreening?uid=<#id#>"
        generated_link = settings.LIVE_URL+"/surveyTemplate?uid=<#id#>"

        data = Prescreener.objects.create(name=name, link=link, enable_otp_verification=enable_otp_verification, project=project) 
        generated_link = settings.LIVE_URL+"/surveyTemplate?uid=<#id#>&screening_id="+str(data.id)
        Prescreener.objects.filter(id=data.id).update(generated_link=generated_link)
        print(data.id)        

        # if question_library_id is not None: 
        #     for questions in question_library_id:
        #         if QuestionLibrary.objects.filter(id=questions).exists():
        #             question_library = PrescreenerQuestionLibrary.objects.create(prescreener_id=data.id, question_library_id=questions)
        #             print("=====",question_library.id)
        #         else:
        #             return Response({'error': {'message': 'question ids not found'}})

        # Page.objects.create(name="Thank You", prescreener_id=data.id)

        Page.objects.create(name="Terminated", prescreener_id=data.id)
        default_page = Page.objects.create(name="Default", prescreener_id=data.id)

        # default_question_id = [106, 172] # instant Insght
        default_question_id = [97, 98] # robas

        for questions in default_question_id:
            PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.create(prescreener_id=data.id, question_library_id=questions, page_id=default_page.id)
            
        return Response({'result': {'panel_duplicate_link': generated_link, 'pre_screener_id': data.id}, 'prescreener': 'prescreener created successfully'})

# @method_decorator([authorization_required], name='dispatch')
class PrescreenerDetailView(APIView):
    def get(self, request, pk):
        if Prescreener.objects.filter(id=pk).exists():
            value = Prescreener.objects.filter(id=pk).values()
            return Response({'result': {'prescreener': value}})
        return Response({'result': {'error': 'no prescreener found'}}, status=HTTP_404_NOT_FOUND)
        

    def put(self, request, pk):
        data = request.data
        name = data.get('name')
        link = data.get('link')
        enable_otp_verification = data.get('enable_otp_verification')
        project = data.get('project')

        if Prescreener.objects.filter(id=pk).exists():
            g_link = Prescreener.objects.get(id=pk).generated_link
            Prescreener.objects.filter(id=pk).update(name=name, link=link, enable_otp_verification=enable_otp_verification, project=project)
            return Response({'result': {'prescreener_id': pk, 'panel_duplicate_link': g_link}, 'message': 'prescreener updated successfully'})
        return Response({'result': {'error': 'no prescreener found to update'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Prescreener.objects.filter(id=pk).exists():
            Prescreener.objects.filter(id=pk).delete()
            return Response({'result': {'prescreener': 'prescreener deleted successfully'}})
        return Response({'result': {'error': 'no prescreener found to delete'}}, status=HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class PrescreenerLogicQuestions(GenericAPIView):
    def get(self, request, pk, p_id):  #send pe-campaign_id in id and page_id in pk

        res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(page_id=pk, is_deleted_question=False).values('question_library_id')
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

        all_pages_for_campaign = Page.objects.filter(prescreener_id=p_id).values()
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

        exclude_page = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.exclude(page_id=pk).values() & PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=p_id).values()
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

@method_decorator([authorization_required], name='dispatch')
class SelectCategoryForCrieteria(GenericAPIView):
    def post(self, request):
        data=request.data

        selected_category_id = data['selected_category_id']
        if selected_category_id:
            cat = QuestionLibrary.objects.filter(question_category_id=selected_category_id).values('question_name', 'id', 'question_type__name', 'is_base_question')
            return Response({'result': {'data': cat}})
        return Response({'result': {'message': 'question category not found'}})

@method_decorator([authorization_required], name='dispatch')
class PrescreenerPageApiView(GenericAPIView):
    def get(self, request): 
        prescreener_id = request.query_params['prescreener_id']
#         print("quryparms===",prescreener_id)

        # if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).exists():
        #     res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).values()
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

        if Page.objects.filter(prescreener_id=prescreener_id).exists():
            final_output = Page.objects.filter(prescreener_id=prescreener_id).values()
            print(final_output)

            return Response({'result': final_output})
        return Response({'error':{'message': 'page not found'}}, status=status.HTTP_404_NOT_FOUND)


# class PrescreenerPageApiView(GenericAPIView):
#     def get(self, request): 
#         prescreener_id = request.query_params['prescreener_id']
#         print("quryparms===",prescreener_id)

#         if PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).exists():
#             res = PeCampaignCampaignPrescreenerQuestionLibraryPage.objects.filter(prescreener_id=prescreener_id).values()
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

import csv
class ImportQuestionAndChoices(APIView):
    def post(self, request):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return Response({'Result': {'Error': 'File Format should be csv'}}, status=status.HTTP_406_NOT_ACCEPTABLE)

        dataset = csv_file.read().decode('UTF-8')
        # print(dataset)               

        return Response("")


from tablib import Dataset
import itertools

def getDuplicatesWithInfo(listOfElems):
    ''' Get duplicate element in a list along with thier indices in list
     and frequency count'''
    dictOfElems = dict()
    index = 0
    # Iterate over each element in list and keep track of index
    for elem in listOfElems:
        
        # If element exists in dict then keep its index in lisr & increment its frequency
        if elem in dictOfElems:
            dictOfElems[elem][0] += 1
            dictOfElems[elem][1].append(index)

        else:
            # Add a new entry in dictionary 
            dictOfElems[elem] = [1, [index]]
        index += 1    
 
    dictOfElems = { key:value for key, value in dictOfElems.items() if value[0] > 1}
    return dictOfElems


@method_decorator([authorization_required], name='dispatch')
class readCampaignExcelData(APIView):
    def post(self, request):

        newQuestionlist = []
        answeVal = []
        data = []
        answeData = []
        question_ids = []
        options_id = []

        question_id_data = []
        options_id_data = []

        questionTypeList = []
        questioncatList = []


        newdataframe = pd.read_csv("/robas/site/public/media/modified.csv" , usecols=['question_id','question_name', 'option_id', 'question_choice', 'question_type','question_category'])
        # newdataframe = pd.read_csv("modified.csv" , usecols=['question_id','question_name', 'option_id', 'question_choice', 'question_type','question_category'])  locally

        print("newdataframe==>", newdataframe)

        for new in newdataframe['question_category']:
            questioncatList.append(new)

        for new in newdataframe['question_type']:
            questionTypeList.append(new)

        for new in newdataframe['question_id']:
            question_ids.append(new)
        
        for new in newdataframe['question_name']:
            newQuestionlist.append(new)

        for new in newdataframe['option_id']:
            options_id.append(new)

        for new in newdataframe['question_choice']:
            answeVal.append(new)

        dictOfElems = getDuplicatesWithInfo(newQuestionlist)
        dictOfQuest = getDuplicatesWithInfo(question_ids)
        dictOfQstType = getDuplicatesWithInfo(questionTypeList)
        dictOfQstCat = getDuplicatesWithInfo(questioncatList)

        # print(dictOfQstType, "===", dictOfQstCat)
        
        for k, l, value,m,n in itertools.zip_longest(dictOfQuest.keys(), dictOfElems.keys(), dictOfQuest.values(), dictOfQstType.keys(), dictOfQstCat.keys()):
            res = QuestionLibrary.objects.create(question_id=k ,question_name=l)

            count = 0
            if count<1:
                for c in value[1]:
                    QuestionLibrary.objects.filter(id=res.id).update(question_type_id=questionTypeList[c], question_category_id=questioncatList[c])
                    count = count+1
            

            res_list = [answeVal[i] for i in  value[1]]
            answeData.append(res_list)

            opt_list = [options_id[i] for i in  value[1]]

            for a, opt in itertools.zip_longest(res_list, opt_list):
                QuestionChoice.objects.create(question_library_id=res.id, name=a, option_id=opt)

        
        panelDat = []
        
        with open("/robas/site/public/media/datasheet.csv" , 'r') as read_obj:
        # with open("datasheet.csv" , 'r') as read_obj:    locally
            # csv_dict_reader = csv.reader(read_obj)  
            csv_dict_reader = csv.DictReader(read_obj)
            # get column namfrom a ces sv file
            column_names = csv_dict_reader.fieldnames
            # print(column_names)
            for row in csv_dict_reader:
                panelDat.append(row)

            print("========")
            
            req_index = column_names.index("Recruitment Source")
            # print(req_index)

            updated_column = column_names[req_index+1:]
            # print(updated_column)

            comman_column = set(updated_column) & set(dictOfQuest.keys())
            # print(comman_column)

        
        question_count = 0
        for i in panelDat:
            if i['Gender'] == "1":
                gender = "male"
            elif i['Gender'] == "2":
                gender = "female"

            usr = UserSurvey.objects.create(panelist_id = i['Panelist id'],status="SOI", email=i['E-mail address'], dob=i['Year of birth'], gender=gender, is_email_verified=False)

            count = 0
            if count < 1:
                print()
                for j in comman_column:
                    # user_email = UserSurvey.objects.get(email=i['E-mail address'])                    
                    if(i[j]!='0'):                        
                        user_qst_id = QuestionLibrary.objects.get(question_id=j)
                        Answer.objects.create(user_survey_id=usr.id, question_library_id=user_qst_id.id, answers=i[j])
                        # print(i['E-mail address'],'\t\t',type(i[j]), "\t\t", type(j))                    
                        count = count +1
                        question_count = question_count + 1
                        print(question_count, "count=", count)

        return Response({"result": "file uploaded successfully"})
        
        