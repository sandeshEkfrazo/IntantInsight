from rest_framework.response import Response
from sampling.models import *
from sampling.serializers import *
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE
from sampling.resource import *
from rest_framework import viewsets
# from tablib import Dataset
from django.utils.decorators import method_decorator
from account.backends_ import *
from projects.pagination import MyPagination
from projects.models import Country, Project
from rest_framework import *
from django.db.models import Q

# Create your views here.
@method_decorator([authorization_required], name='dispatch')
class SamplingAPIView(viewsets.ModelViewSet):
    serializer_class = SamplingSerializer

    def get_queryset(self):
        if self.request.query_params:
            sample_obj = Sampling.objects.filter(project_id=self.request.query_params['pid'])
            return sample_obj
        else:
            allval = Sampling.objects.all()
            return allval

    def retrieve(self, request, *args, **kwargs):
        try:
            sample_obj = Sampling.objects.get(id=kwargs['pk'])
            serializer = SamplingSerializer(sample_obj)
            return Response(serializer.data)
        except :
            return Response({"ERROR":"INVALID SAMPLE ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)
            
    def create(self, request):
        serializer = SamplingSerializer(data=request.data)
        

        if serializer.is_valid():
            # sample_obj = serializer.save()
            if Sampling.objects.filter(name=request.data['name']).exists():
                return Response({'error': 'sample name already exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                
            Sampling.objects.create(
                name = request.data['name'],
                complete = request.data['complete'],
                bonus_points = request.data['bonus_points'],
                is_custom_panel = request.data['is_custom_panel'],
                quotas_id = request.data['quotas'],
                project_id = request.data['project']
            )

            # project_obj = Project.objects.get(id=serializer.data['project'])
            project_obj = Project.objects.get(id=request.data['project'])

            # maretr = []
            # for i in project_obj.country:
            #     marketer = Country.objects.filter(id=i['id']).values()
            #     for m in marketer:
            #         maretr.append(m['name'])

            # updated_sampling_obj = Sampling.objects.get(id=sample_obj.id)
            # updated_serializer_data = SamplingSerializer(updated_sampling_obj)

            updated_serializer_data = SamplingSerializer(project_obj)

            # return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK", "data": updated_serializer_data.data, "market_name":maretr, "project_name": project_obj.name, "project_id": project_obj.id})  

            return Response({"MESSAGE":"SUCCESS", "STATUS": "200 OK"}) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

    def update(self, request, *args, **kwargs):
        if Sampling.objects.filter(~Q(id=kwargs['pk']) & Q(name = request.data['name'])).exists():
            return Response({'error': 'sample name already exist'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if Sampling.objects.filter(id=kwargs['pk']).exists():
            sample_obj = Sampling.objects.get(id=kwargs['pk'])
            serializer = SamplingSerializer(sample_obj, data=request.data, partial=True)
            if serializer.is_valid():
                Sampling.objects.filter(id=kwargs['pk']).update(
                name = request.data['name'],
                complete = request.data['complete'],
                bonus_points = request.data['bonus_points'],
                is_custom_panel = request.data['is_custom_panel'],
                quotas_id = request.data['quotas'],
                project_id = request.data['project']
            )
                return Response({"MESSAGE": "SUCCESS", "STATUS": "200 OK", "data": serializer.data})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return Response({"ERROR":"INVALID SAMPLE ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)

        # try:
        #     sample_obj = Sampling.objects.get(id=kwargs['pk'])
        #     serializer = SamplingSerializer(sample_obj, data=request.data, partial=True)
        #     if serializer.is_valid():
        #         samp_obj = serializer.save()

        #         project_obj = Project.objects.get(id=serializer.data['project'])

        #         maretr = []
        #         for i in project_obj.country:
        #             marketer = Country.objects.filter(id=i['id']).values()
        #             for m in marketer:
        #                 maretr.append(m['name'])

        #         return Response({"MESSAGE": "SUCCESS", "STATUS": "200 OK", "data": serializer.data, "market_name":maretr, "project_name": project_obj.name})
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        # except:
        #     return Response({"ERROR":"INVALID SAMPLE ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            sample_obj = self.get_object()
            sample_obj.delete()
            return Response({"MESSAGE": "SUCCESS", "STATUS": "204 NO CONTENT"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"ERROR":"INVALID ID", "STATUS": "404 NOT FOUND"}, status=HTTP_404_NOT_FOUND)



# class ListOfSample(ListAPIView):
#     serializer_class = SamplingSerializer
#     queryset = Sampling.objects.all()
#     pagination_class = MyPagination

# class SamplingAPIView(GenericAPIView):
#     def get(self, request, pk):
#         if Sampling.objects.filter(project_id=pk).exists():
#             values = Sampling.objects.filter(project_id=pk).values()
#             return Response({'result': {'sampling': values}})
#         return Response({'result': {'sampling': 'sampling not found'}})

#     def post(self, request):
#         data = request.data

#         name = data['name']
#         complete = data['complete']
#         bonus_points = data['bonus_points']
#         is_custom_panel = data['is_custom_panel']
#         # is_exclusive = data['is_exclusive']
#         project = data['project']

#         if Sampling.objects.filter(name=name).exists():
#             return Response({'result': {'error': 'name already taken'}}, status=HTTP_406_NOT_ACCEPTABLE)
#         sampling = Sampling.objects.create(name=name, complete=complete, bonus_points=bonus_points, is_custom_panel=is_custom_panel, project_id=project)

#         project_name = Project.objects.get(id=project)



#         print(project_name.country)

#         maretr = []
#         for i in project_name.country:
#             print(i)
#             marketer = Country.objects.filter(id=i['id']).values()
#             for m in marketer:
#                 print(m['name'])
#                 maretr.append(m['name'])

#         return Response({'result': {'sample_id': sampling.id, 'sample_name': sampling.name, 'project_id': project, 'project_name': project_name.name, 'market_name':maretr}, 'message': 'sampling created successfully'})
    
#     def put(self, request, pk):
#         data = request.data

#         name = data['name']
#         complete = data['complete']
#         bonus_points = data['bonus_points']
#         is_custom_panel = data['is_custom_panel']
#         # is_exclusive = data['is_exclusive']
#         project = pk

#         if Sampling.objects.filter(project_id=pk).exists():
#             Sampling.objects.filter(project_id=pk).update(name=name, complete=complete, bonus_points=bonus_points, is_custom_panel=is_custom_panel, project_id=project)

#             pro = Project.objects.get(id=pk)


#             print(pro.country)

#             maretr = []
#             for i in pro.country:
#                 marketer = Country.objects.filter(id=i['id']).values()
#                 for m in marketer:
#                     print(m['name'])
#                     maretr.append(m['name'])            

#             res = Sampling.objects.get(project_id=pk)
#             sample_id = res.id
#             sample_name = res.name
            
#             return Response({'result': {'sample_id': sample_id, 'sample_name': sample_name, 'project_id': pk, 'project_name': pro.name, 'market_name': maretr} , 'sampling': 'sampling updated successfully'})
#         return Response({'result': {'sampling': 'sampling not found to update fo this project'}})




# class UploadExcel(APIView):
#     def post(self, request):
#             person_resource = PersonResource()
#             dataset = Dataset()
#             new_persons = request.FILES['new_persons']
            
#             imported_data = dataset.load(new_persons.read(),format='xlsx')
#             for i in imported_data:
#                 value = Person(
#                     i[0], i[1], i[2],i[3],i[4]
#                 )
#                 value.save()
#             return  Response({'result': {'message': 'file uploaded successfully'}})


