from functools import reduce
from operator import and_
from .views import *
from django.db.models.functions import Cast
from django.db.models import IntegerField

def filterProject(queryset, query_params):
    
    query_filters = []

    start_date = query_params.get('start_date_time')
    end_date = query_params.get('end_date_time')
    status = query_params.get('status')
    search_name = query_params.get('search')
    is_deleted_projet = query_params.get('is_deleted')
    should_paginate = query_params.get('paginate', False)
    sort_by = query_params.get('sort_by')
    sort_type = query_params.get('sort_type')


    if start_date:
        start_date_and_time = datetime.datetime.utcfromtimestamp(int(start_date)/1000) 
        query_filters.append(Q(is_deleted=False) & (Q(start_date__gte=start_date_and_time)))

    if end_date:
        one_day_extra = timedelta(days=1)
        end_date_and_time = datetime.datetime.utcfromtimestamp(int(end_date)/1000) + one_day_extra
        query_filters.append(Q(is_deleted=False) & (Q(end_date__lte=end_date_and_time)))

    if status:
        query_filters.append(Q(status=status) & Q(is_deleted=False))

    if search_name:
        query_filters.append(
            Q(Q(name__icontains=search_name) | Q(status__icontains=search_name) | Q(market_type__icontains=search_name) | Q(created_by__first_name__icontains=search_name) | Q(client__clientname__icontains=search_name) |  Q(company__name__icontains=search_name) |  Q(id__icontains=search_name)) & Q(is_deleted=False)
        )

    if is_deleted_projet:
        query_filters.append(Q(is_deleted=True))

    if sort_by:
        if sort_type == "1":
            if sort_by == 'total_complete':
                queryset = queryset.annotate(
                    total_complete_int=Cast('total_complete', IntegerField())
                ).order_by('total_complete_int')
            else:
                queryset = queryset.order_by(f"{sort_by}")
        if sort_type == "-1":
            if sort_by == 'total_complete':
                queryset = queryset.annotate(
                    total_complete_int=Cast('total_complete', IntegerField())
                ).order_by('-total_complete_int')
            else:
                queryset = queryset.order_by(f"-{sort_by}")

    if query_filters:
        combined_query = reduce(and_, query_filters)
        return queryset.filter(combined_query)
    else:
        return queryset

    

        

