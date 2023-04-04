from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from datetime import datetime
from rest_framework.status import *
from django.utils.decorators import method_decorator
from account.backends_ import *

@method_decorator([authorization_required], name='dispatch')
class ServiveApiView(APIView):
    # serializer_class = ServiceSerializer
    # queryset = Service.objects.all()
    # pagination_class = MyPagination
    def get(self, request):
        if request.query_params.get('id'):
            all_values = Service.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = Service.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if Service.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exists'}}, status=HTTP_406_NOT_ACCEPTABLE)

        else:
            Service.objects.create(name=name,
                                   create_timestamp=timestamp, last_update_timestamp=timestamp)
            return Response({'result': {'service': 'service created successfully'}})

    def put(self, request, pk):
        data = request.data
        name = data.get('name')
        company = data.get('company')
        now = datetime.now()
        # timestamp = datetime.timestamp(now)

        if Service.objects.filter(id=pk).exists():
            Service.objects.filter(id=pk).update(
                name=name, last_update_timestamp=now)
            return Response({'result': {'Service': 'service updated successfully'}})
        else:
            return Response({'result': {'error': 'service not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Service.objects.filter(id=pk).exists():
            Service.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'service deleted successfully'}})
        return Response({'result': {'error': 'service id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class ProjectTypeApiView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = ProjectType.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = ProjectType.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        company = data.get('company')
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if ProjectType.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exists'}}, status=HTTP_406_NOT_ACCEPTABLE)

        else:
            ProjectType.objects.create(
                name=name, company=company, create_timestamp=timestamp, last_update_timestamp=timestamp)
            return Response({'result': {'project_type': 'project_type created successfully'}})

    def put(self, request, pk):
        data = request.data
        name = data.get('name')
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if ProjectType.objects.filter(id=pk).exists():
            ProjectType.objects.filter(id=pk).update(
                name=name, last_update_timestamp=timestamp)
            return Response({'result': {'project_type': 'project_type updated successfully'}})
        else:
            return Response({'result': {'error': 'project not found'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if ProjectType.objects.filter(id=pk).exists():
            ProjectType.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'projectType deleted successfully'}})
        return Response({'result': {'error': 'projectType id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class CurrencyApiView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = Currency.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = Currency.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        symbol = data.get('symbol')
        if Currency.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already Exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            Currency.objects.create(name=name, symbol=symbol)
            return Response({'result': {'currency': 'currency created successfully'}})

    def delete(self, request, pk):
        if Currency.objects.filter(id=pk).exists():
            Currency.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'currency deleted successfully'}})
        return Response({'result': {'error': 'currency id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class CategoryView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = Category.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = Category.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        detail = data.get('detail')

        if Category.objects.filter(name=name).exists():
            return Response({'result': {'error': 'Name already Exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            Category.objects.create(name=name, detail=detail)
            return Response({'result': {'category': 'category created successfully'}})

    def delete(self, request, pk):
        if Category.objects.filter(id=pk).exists():
            Category.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'category deleted successfully'}})
        return Response({'result': {'error': 'category id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class QuotasApiView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = Quotas.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = Quotas.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')

        if Quotas.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            Quotas.objects.create(name=name)
            return Response({'result': {'quotas': 'quotas created successfully'}})

    def delete(self, request, pk):
        if Quotas.objects.filter(id=pk).exists():
            Quotas.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'quotas deleted successfully'}})
        return Response({'result': {'error': 'quotas id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

# @method_decorator([authorization_required], name='dispatch')
class CountryApiView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = Country.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = Country.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data.get('name')
        symbol = data.get('symbol')

        if Country.objects.filter(name=name).exists():
            return Response({'result': {'error': 'Name Lready exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            Country.objects.create(name=name, symbol=symbol)
            return Response({'result': {'country': 'country created successfully'}})

    def delete(self, request, pk):
        if Country.objects.filter(id=pk).exists():
            Country.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'country deleted successfully'}})
        return Response({'result': {'error': 'country id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class B2BApi(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = B2B.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = B2B.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data

        name = data['name']

        if B2B.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exist'}})
        else:
            B2B.objects.create(name=name)
            return Response({'result': {'b2b': 'b2b created successfully'}})

    def delete(self, request, pk):
        if B2B.objects.filter(id=pk).exists():
            B2B.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'B2B deleted successfully'}})
        return Response({'result': {'error': 'B2B id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class B2CApi(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = B2C.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = B2C.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data

        name = data['name']

        if B2C.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exist'}})
        else:
            B2C.objects.create(name=name)
            return Response({'result': {'b2b': 'b2b created successfully'}})

    def delete(self, request, pk):
        if B2C.objects.filter(id=pk).exists():
            B2C.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'B2C deleted successfully'}})
        return Response({'result': {'error': 'B2C id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class SurevyTopicApi(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = SurveyTopic.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = SurveyTopic.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data

        name = data['name']
        if SurveyTopic.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already exist'}})
        else:
            SurveyTopic.objects.create(name=name)
            return Response({'result': {'survey topic': 'surevy topic created successfully'}})

    def delete(self, request, pk):
        if SurveyTopic.objects.filter(id=pk).exists():
            SurveyTopic.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'surveyTopic deleted successfully'}})
        return Response({'result': {'error': 'surveyTopic id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class ClientApiView(APIView):
    # serializer_class = ClientSerializer
    # queryset = Client.objects.all()
    # pagination_class = MyPagination

    def get(self, request):
        pk = request.query_params.get('id')
        if pk:
            all_values = Client.objects.filter(id=pk).values()
            return Response({"result": all_values})
        else:
            all_values = Client.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        clientname = data.get('clientname')
        address = data.get('address')
        email = data.get('email')
        website = data.get('website')
        company = data.get('company')
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if Client.objects.filter(clientname=clientname).exists():
            if Client.objects.filter(email=email).exists():
                return Response({'result': {'error': 'email already taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
            return Response({'result': {'error': 'client name already exists'}}, status=HTTP_406_NOT_ACCEPTABLE)
        else:
            Client.objects.create(clientname=clientname, address=address, email=email, website=website,
                                  company=company, create_timestamp=timestamp, last_update_timestamp=timestamp)
            return Response({'result': {'client': 'client created successfully'}})

    def put(self, request, pk):
        data = request.data
        clientname = data.get('clientname')
        address = data.get('address')
        email = data.get('email')
        website = data.get('website')
        company = data.get('company')
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        if Client.objects.filter(id=pk).exists():
            Client.objects.filter(id=pk).update(clientname=clientname, address=address, email=email, website=website,
                                                company=company, last_update_timestamp=timestamp)
            return Response({'result': {'client': 'client updated successfully'}})
        return Response({'result': {'error': 'client not found to update'}}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if Client.objects.filter(id=pk).exists():
            Client.objects.filter(id=pk).delete()
            return Response({"result": {'client': 'client deleted successfully'}})
        return Response({'result': {'error': 'client not found delete'}}, status=HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class getSurveyStatus(APIView):
    def post(self, request):
        data = request.data

        company = data['company']
        if SurveyStatus.objects.filter(company=company).exists():
            values = SurveyStatus.objects.filter(company=company).values()
            return Response({'result': {'survey_status': values}})
        return Response({'error': {'message': 'survey status not found'}})

@method_decorator([authorization_required], name='dispatch')
class SurveyStatusView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = SurveyStatus.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = SurveyStatus.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data['name']
        message = data['message']
        company = data['company']

        SurveyStatus.objects.create(
            name=name, message=message, company=company)
        return Response({'result': {"survey status": "syrvey status created succesfully"}})

    def delete(self, request, pk):
        if SurveyStatus.objects.filter(id=pk).exists():
            SurveyStatus.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'survey status deleted successfully'}})
        return Response({'result': {'error': 'survey status id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class CampaignTypeView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = CampaignType.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = CampaignType.objects.all().values()
            return Response({"result": all_values})

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

@method_decorator([authorization_required], name='dispatch')
class CommissionModelView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = CommissionModel.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = CommissionModel.objects.all().values()
            return Response({"result": all_values})

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

@method_decorator([authorization_required], name='dispatch')
class PeCampaignTypeView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = PeCampaignType.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = PeCampaignType.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data['name']

        if PeCampaignType.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}})
        PeCampaignType.objects.create(name=name)
        return Response({'result': {'pe_campaign_type': 'pe campaign created successfully'}})

    def delete(self, request, pk):
        if PeCampaignType.objects.filter(id=pk).exists():
            PeCampaignType.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'PeCampaignType deleted successfully'}})
        return Response({'result': {'error': 'PeCampaignType id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)

@method_decorator([authorization_required], name='dispatch')
class PeCategoryView(APIView):
    def get(self, request):
        if request.query_params.get('id'):
            all_values = PeCategory.objects.filter(id=request.query_params.get('id')).values()
            return Response({"result": all_values})
        else:
            all_values = PeCategory.objects.all().values()
            return Response({"result": all_values})

    def post(self, request):
        data = request.data
        name = data['name']

        if PeCategory.objects.filter(name=name).exists():
            return Response({'result': {'error': 'name already taken'}})
        PeCategory.objects.create(name=name)
        return Response({'result': {'pe_pategory': 'pe category created successfully'}})

    def delete(self, request, pk):
        if PeCategory.objects.filter(id=pk).exists():
            PeCategory.objects.filter(id=pk).delete()
            return Response({'result': {'message': 'PeCategory deleted successfully'}})
        return Response({'result': {'error': 'PeCategory id not found to delete'}}, status=status.HTTP_404_NOT_FOUND)
