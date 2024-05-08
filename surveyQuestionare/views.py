from os import name
from django.core.checks import messages
from django.core.checks.messages import Error
from django.db.models.expressions import Col
from django.http.response import Http404, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.utils import decorators
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from rest_framework import status
import rest_framework
from rest_framework import views
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from projects.pagination import MyPagination

from surveyQuestionare.serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from functools import wraps
from django.utils.decorators import method_decorator
from account.backends_ import *
# Create your views here.

# @method_decorator([authorization_required], name='dispatch')
class ElementListApiView(ListAPIView):
    serializer_class = ElementSerializer
    queryset = Element.objects.all()
    # pagination_class = MyPagination

class OptionListApiView(ListAPIView):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    # pagination_class = MyPagination

class QuestionListApiView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    pagination_class = MyPagination

class SureveyGoalListApiView(ListAPIView):
    serializer_class = SurveyGoalSerializer
    queryset = SurveyGoal.objects.all()
    pagination_class = MyPagination

class IndustryTypeListApiView(ListAPIView):
    serializer_class = IndustryTypeSerializer
    queryset = IndustryType.objects.all()
    pagination_class = MyPagination

class SurveyCategoryListApiView(ListAPIView):
    serializer_class = SurveyCategorySerializer
    queryset = SurveyCategory.objects.all()
    pagination_class = MyPagination

class SurveyListApiView(ListAPIView):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    pagination_class = MyPagination

class DocumentListApiView(ListAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    pagination_class = MyPagination

class QuotasListApiView(ListAPIView):
    serializer_class = QuotasSerializer
    queryset = QuotasSQ.objects.all()
    pagination_class = MyPagination
  
class AttributesListApiView(ListAPIView):
    serializer_class = AttributesSerializer
    queryset = Attributes.objects.all()
    pagination_class = MyPagination

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# @method_decorator([need_jwt_verification], name='dispatch')
class SurveyGoalApiView(GenericAPIView):
    def get(self,request, pk):
        if SurveyGoal.objects.filter(id=pk).exists():
            list_data = SurveyGoal.objects.filter(id=pk).values()
            return Response({'result': {'survey_goal': list_data}})
        return Response({'error': {'message': 'survey goal not found'}}, status=HTTP_404_NOT_FOUND)

    def post(self,request):
        data = request.data
        name = data.get('name')
        description= data.get('description')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if SurveyGoal.objects.filter(name=name).exists():
            return Response({'error': {'message': 'survey name already exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            SurveyGoal.objects.create(name=name,
                                        description=description,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result':{'message': 'survey goal created successfully'}})

    def put(self,request,pk):
        data = request.data

        name = data.get('name')
        description= data.get('description')
        last_update_timestamp= data.get('last_update_timestamp')

        if SurveyGoal.objects.filter(id=pk).exists():
            SurveyGoal.objects.filter(id=pk).update(name=name,
                                        description=description,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result': {'message': 'Updated Successfully'}})
        else:
            return Response({'error': {'message': 'survey goal not found'}}, status=HTTP_404_NOT_FOUND)
            

    def delete(self, request, pk):
        if SurveyGoal.objects.filter(id=pk).exists():
            SurveyGoal.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'SurveyGoal deleted successfully'}})
        return Response({'result': {'error': 'SurveyGoal id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)



class IndustryTypeApiView(GenericAPIView):
    def get(self,request, pk):
        if IndustryType.objects.filter(id=pk).exists():
            list_data = IndustryType.objects.filter(id=pk).values()
            return Response({'result': {'industry_type': list_data}})
        return Response({'error': {'message': 'industry type not found'}}, status=HTTP_404_NOT_FOUND)

    def post(self,request):
        data = request.data
        name = data.get('name')
        description= data.get('description')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if IndustryType.objects.filter(name=name).exists():
            return Response({'error':'industry name already exists'})
        else:
            IndustryType.objects.create(name=name,
                                        description=description,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data

        name = data.get('name')
        description= data.get('description')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if IndustryType.objects.filter(name=name).exists():
            return Response({'error':'industry name already exists'})
        else:
            IndustryType.objects.filter(id=pk).update(name=name,
                                        description=description,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result':'Updated Successfully'})

    def delete(self, request, pk):
        if IndustryType.objects.filter(id=pk).exists():
            IndustryType.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'IndustryType deleted successfully'}})
        return Response({'result': {'error': 'IndustryType id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

class SurveyCategoryApiView(GenericAPIView):
    def get(self,request):
        list_data = SurveyCategory.objects.all().values()
        return Response({'result':list_data})

    def post(self,request):
        data = request.data
        name = data.get('name')
        description= data.get('description')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if SurveyCategory.objects.filter(name=name).exists():
            return Response({'error':'survey category already exists'})
        else:
            SurveyCategory.objects.create(name=name,
                                        description=description,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data

        name = data.get('name')
        description= data.get('description')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')

        if SurveyCategory.objects.filter(name=name).exists():
            return Response({'error':'survey category already exists'})
        else:
            SurveyCategory.objects.filter(id=pk).update(name=name,
                                        description=description,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp)

            return Response({'result':'Updated Successfully'})

    def delete(self, request, pk):
        if SurveyCategory.objects.filter(id=pk).exists():
            SurveyCategory.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'SurveyCategory deleted successfully'}})
        return Response({'result': {'error': 'SurveyCategory id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

class SurveyApiView(GenericAPIView):
    def get(self,request,pk):
        if(Survey.objects.filter(id=pk).exists()):
            list_data = Survey.objects.filter(id=pk).values()
            return Response({'result':list_data})
        return Response({'result': 'survey id not found'}, status=HTTP_404_NOT_FOUND)

    def post(self,request):
        data = request.data
        name  = data.get('name')
        surveycategory= data.get('surveycategory_id')
        type_of_responses= data.get('type_of_responses')
        survey_format= data.get('survey_format')
        number_of_responses= data.get('number_of_responses')
        estimate_cost= data.get('estimate_cost')
        estimated_completion_date= data.get('estimated_completion_date')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')
        state= data.get('state')
        user= data.get('user_id')
        live_survey_link= data.get('live_survey_link')
        test_survey_link= data.get('test_survey_link')
        description= data.get('description')
        tags= data.get('tags')
        directory= data.get('directory')
        primary_language= data.get('primary_language')
        surveygoal= data.get('surveygoal_id')
        industrytype= data.get('industrytype_id')

        if Survey.objects.filter(name=name).exists():
            return Response({'error':'survey name already exists'})
        else:
            survey =  Survey.objects.create(name=name,
                                        surveycategory_id=surveycategory,
                                        type_of_responses=type_of_responses,
                                        survey_format=survey_format,
                                        number_of_responses=number_of_responses,
                                        estimate_cost=estimate_cost,
                                        estimated_completion_date=estimated_completion_date,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp,
                                        state=state,
                                        user_id=user,
                                        live_survey_link=live_survey_link,
                                        test_survey_link=test_survey_link,
                                        description=description,
                                        tags=tags,
                                        directory=directory,
                                        primary_language=primary_language,
                                        surveygoal_id=surveygoal,
                                        industrytype_id=industrytype)

            return Response({'survey_id': survey.id ,'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data
        name  = data.get('name')
        surveycategory= data.get('surveycategory_id')
        type_of_responses= data.get('type_of_responses')
        survey_format= data.get('survey_format')
        number_of_responses= data.get('number_of_responses')
        estimate_cost= data.get('estimate_cost')
        estimated_completion_date= data.get('estimated_completion_date')
        create_timestamp= data.get('create_timestamp')
        last_update_timestamp= data.get('last_update_timestamp')
        state= data.get('state')
        user= data.get('user_id')
        live_survey_link= data.get('live_survey_link')
        test_survey_link= data.get('test_survey_link')
        description= data.get('description')
        tags= data.get('tags')
        directory= data.get('directory')
        primary_language= data.get('primary_language')
        surveygoal= data.get('surveygoal_id')
        industrytype= data.get('industrytype_id')

        if Survey.objects.filter(id=pk).exists():
            survey = Survey.objects.filter(name=name).update(name=name,
                                        surveycategory_id=surveycategory,
                                        type_of_responses=type_of_responses,
                                        survey_format=survey_format,
                                        number_of_responses=number_of_responses,
                                        estimate_cost=estimate_cost,
                                        estimated_completion_date=estimated_completion_date,
                                        create_timestamp=create_timestamp,
                                        last_update_timestamp=last_update_timestamp,
                                        state=state,
                                        user_id=user,
                                        live_survey_link=live_survey_link,
                                        test_survey_link=test_survey_link,
                                        description=description,
                                        tags=tags,
                                        directory=directory,
                                        primary_language=primary_language,
                                        surveygoal_id=surveygoal,
                                        industrytype_id=industrytype)

            return Response({'survey_id': pk,'result':'Updated Successfully'})
        else:
            return Response({'error':'survey name already exists'}, status=HTTP_404_NOT_FOUND)
           

    def delete(self,request,pk):
        if Survey.objects.filter(id=pk).exists():
            delete_data = Survey.objects.filter(id=pk).delete()
            return Response({'result':'survey deleted sucessfully'})
        return Response({'result':'survey id not found to delete'}, status=HTTP_404_NOT_FOUND)


class DocumentApiView(GenericAPIView):
    def get(self,request):
        list_data = Document.objects.all().values()
        return Response({'result':list_data})

    def post(self,request):
        data = request.data
        doc_1=data.get('doc_1')
        doc_2=data.get('doc_2')
        doc_3 =data.get('doc_3')
        survey=data.get('survey_id')

        if Document.objects.filter(doc_1=doc_1).exists():
            return Response({'error':'survey id already exists'})
        else:
            Document.objects.create(doc_1=doc_1,
                                            doc_2=doc_2,doc_3=doc_3,
                                             survey_id=survey  )

            return Response({'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data

        data = request.data
        doc_1=data.get('doc_1')
        doc_2=data.get('doc_2')
        doc_3 =data.get('doc_3')
        survey=data.get('survey_id')

        if Document.objects.filter(doc_1=doc_1).exists():
            return Response({'error':'document name already exists'})
        else:
            Document.objects.filter(id=pk).update(doc_1=doc_1,
                                            doc_2=doc_2,doc_3=doc_3,
                                             survey_id=survey  )


            return Response({'result':'Updated Successfully'})

    def delete(self,request,pk):
        delete_data = Document.objects.filter(id=pk).delete()
        return Response({'result':delete_data})



class QuotasApiView(GenericAPIView):
    def get(self,request):
        list_data = QuotasSQ.objects.all().values()
        return Response({'result':list_data})

    def post(self,request):
        data = request.data
        name =data.get('name')

        survey=data.get('survey_id')

        if QuotasSQ.objects.filter(name=name).exists():
            return Response({'error':'id already exists'})
        else:
            QuotasSQ.objects.create(name=name,
                                             survey_id=survey  )

            return Response({'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data

        name =data.get('name')

        survey=data.get('survey_id')

        if QuotasSQ.objects.filter(name=name).exists():
            return Response({'error':'id already exists'})
        else:
            QuotasSQ.objects.filter(id=pk).update(name=name,
                                             survey_id=survey)


            return Response({'result':'Updated Successfully'})

    def delete(self,request,pk):
        delete_data = QuotasSQ.objects.filter(id=pk).delete()
        return Response({'result':delete_data})


class AttributesApiView(GenericAPIView):
    def get(self,request):
        list_data = Attributes.objects.all().values()
        return Response({'result':list_data})

    def post(self,request):
        data = request.data
        name =data.get('name')

        limit=data.get('limit')
        total=data.get('total')
        need=data.get('need')

        if Attributes.objects.filter(name=name).exists():
            return Response({'error':'id already exists'})
        else:
            Attributes.objects.create(name=name,
                                             limit=limit,
                                            total=total,
                                            need =need)

            return Response({'result':'Created Successfully'})

    def put(self,request,pk):
        data = request.data
        name =data.get('name')
        limit=data.get('limit')
        total=data.get('total')
        need=data.get('need')

        if Attributes.objects.filter(name=name).exists():
            return Response({'error':'id already exists'})
        else:
            Attributes.objects.filter(id=pk).update(name=name,
                                             limit=limit,
                                            total=total,
                                            need =need)


            return Response({'result':'Updated Successfully'})

    def delete(self,request,pk):
        delete_data = Attributes.objects.filter(id=pk).delete()
        return Response({'result':delete_data})


class ElementApiView(APIView):
    def get(self,request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if Element.objects.filter(id=pk).exists():
            ele = Element.objects.get(id=pk)
            print(ele.name)
            response = {'option_id': '', 'option_name': '', 'option_type': ''}
            data = []
            
            eleopt = ElementOption.objects.filter(element_id=pk).values()
            for i in eleopt:
                opt = Option.objects.get(id=i['option_id'])
                response['option_id'] = opt.id
                response['option_name'] = opt.name
                response['option_type'] = opt.option_type

                data.append(response)
                response = {'option_id': '', 'option_name': '', 'option_type': ''}
            
            return Response({'result': {'element_name': ele.name ,'options': data}})
        return Response({'error': {'message': 'element not found'}}, status=HTTP_404_NOT_FOUND)
        
    def post(self, request):
        data = request.data

        name = data['name']
        options = data['options']

        if Element.objects.filter(name=name).exists():
            return Response({'result': {'message': 'name already exist'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            ele = Element.objects.create(name=name)
            for i in options:
                if (Q(Option.objects.filter(id=i).exists()) & Q(Element.objects.filter(name=name).exists())) :
                    print(i)    
                    ElementOption.objects.create(element_id=ele.id, option_id=i)
        return Response({'result': {'element_id': ele.id}, 'message': 'element created successfully'}) 
        

    def delete(self, request, pk):
        if Element.objects.filter(id=pk).exists():
            Element.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'Element deleted successfully'}})
        return Response({'result': {'error': 'Element id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)
        

class OptionsApiView(GenericAPIView):
    def get(self, pk):
        if Option.objects.filter(id=pk).exists():
            val = Option.objects.filter(id=pk).values()
            return Response({"result": val})
        return Response({'error': {'message': 'options not found'}}, status=HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        
        name = data['name']
        option_type = data['option_type']

        if Option.objects.filter(Q(option_type=option_type) & Q(name=name)).exists():
            return Response({'result': {'message': 'option_type already exist for this option'}}, status=HTTP_406_NOT_ACCEPTABLE)
        opt = Option.objects.create(name=name, option_type=option_type)
        return Response({'result': {'options_id': opt.id, 'message': 'option created successfully'}})

    def delete(self, request, pk):
        if Option.objects.filter(id=pk).exists():
            Option.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'Option deleted successfully'}})
        return Response({'result': {'error': 'Option id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)


class SurveyQuestionApiView(GenericAPIView):
    def get(self, request, pk):
        if Questions.objects.filter(id=pk).exists():
            question = Questions.objects.get(id=pk)
            data = []
            res = {'option': ''}
            quest_opt = QuestionOptions.objects.filter(question_id=pk).values()
            print(quest_opt)
            for i in quest_opt:
                print(i)
                res['option'] = i['name']
                data.append(res)
                res = {'option': ''}
            return Response({'result': {'question': question.name, 'option': data}}, status=HTTP_404_NOT_FOUND)
        return Response({'error': {'message': 'question not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Questions.objects.filter(id=pk).exists():
            Questions.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'question deleted successfully'}})
        return Response({'error': {'message': 'question not found to delete'}}, status=HTTP_404_NOT_FOUND)
        

    # def put(self, request, pk):
    #     data = request.data

    #     name = data['name']
    #     element_id =  data['element_id']
    #     column = data['column']
    #     question_options = data['question_options']
    #     conditions = data['conditions']

    #     if Questions.objects.filter(id=pk).exists():
    #         if Element.objects.filter(id=element_id).exists():
    #             question = Questions.objects.filter(id=pk).update(name=name, element_id=element_id, column=column, conditions=conditions)
                
    #         else:
    #             return Response({'error': {'message': 'element not found'}}, status=HTTP_404_NOT_FOUND)

    #         list_opt_id = QuestionOptions.objects.filter(question_id=pk).values('id')
            
    #         if question_options is not None: 
    #             for values in question_options:
    #                 print()
    #             for i in list_opt_id:
    #                 print(i)
    #                 # print()
    #                 # print(values)
    #                     # val = QuestionOptions.objects.filter(id=i['id']).update(name=values['name'])
    #                     # print(val)

            
    #     else:
    #         return Response({'error': {'message': 'question not found'}})
    #     return Response({'result': {'message': 'question updated successfully'}})

    def post(self, request):
        data = request.data

        name = data['name']
        element_id =  data['element_id']
        column = data['column']
        question_options = data['question_options']
        conditions = data['conditions']

        if Questions.objects.filter(name=name).exists():
            return Response({"error": {'message': 'question name alredy exist'}}, status=HTTP_406_NOT_ACCEPTABLE)
        if Element.objects.filter(id=element_id).exists():
                question = Questions.objects.create(name=name, element_id=element_id, column=column, conditions=conditions)
        else:
            return Response({'error': {'message': 'element not found'}}, status=HTTP_404_NOT_FOUND)

        if question_options is not None:
            for values in question_options:
                value = QuestionOptions.objects.create(name=values['name'], question_id=question.id)   

        return Response({'result': {'question_id': question.id}, 'message': 'question created successfully'})


class SurveyQuestionarePage(APIView):
    def post(self, request):
        data = request.data

        page_name = data['page_name']
        question_ids = data['question_ids']
        survey_id = data['survey_id']

        if SurveyPage.objects.filter(name = page_name).exists():
            return Response({'result': {'message': 'page name already exist'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            survey_page = SurveyPage.objects.create(name = page_name, survey_id=survey_id)

            if question_ids is not None:
                for i in question_ids:
                    print(i)
                    SurveyPanelQuestion.objects.create(survey_id=survey_id, question_id=i, survey_page_id=survey_page.id)
            else:
                return Response({'result': {'message': 'question_id not found'}}, status=HTTP_404_NOT_FOUND)

        return Response({'result':{'message': 'page created successfully'}})

class PanelistPeCampaignAnswer(APIView):
    def post(self, request):
        data = request.data
        panelist_id = data['panelist_id']
        answered_question = data['answered_question']
        
        if SurveyQuestionareSurvey.objects.filter(panelist_id=panelist_id).exists():
            return Response({'error': {'message': 'sorry you have already attended this survey'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            for i in answered_question:
                for j in i['option_id']:
                    data = SurveyQuestionareSurvey.objects.create(panelist_id=panelist_id ,question_id=i['question_id'], option_id=j)
            return Response({'result': {'message': 'Thank you for your response'}})

