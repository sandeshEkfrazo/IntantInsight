from functools import reduce
from operator import and_
from .views import *
from django.db.models.functions import Cast
from datetime import timedelta
from django.db.models import IntegerField

def filterCampaign(queryset, query_params):
    
    query_filters = []

    start_date = query_params.get('start_date_time')
    end_date = query_params.get('end_date_time')
    search_name = query_params.get('search')
    is_deleted = query_params.get('is_deleted')
    sort_by = query_params.get('sort_by')
    sort_type = query_params.get('sort_type')

    
    if start_date:
        one_day_extra = timedelta(days=1)
        start_date_and_time = datetime.datetime.utcfromtimestamp(int(start_date)/1000) + one_day_extra
        query_filters.append(Q(is_deleted=False) & (Q(start_date__gte=start_date_and_time)))

    if end_date:
        one_day_extra = timedelta(days=1)
        end_date_and_time = datetime.datetime.utcfromtimestamp(int(end_date)/1000) + one_day_extra
        query_filters.append(Q(is_deleted=False) & (Q(end_data__lte=end_date_and_time)))

    

    if search_name:
        query_filters.append(
            Q(Q(campaign_name__icontains=search_name) | Q(status__icontains=search_name) | Q(campaign_type__name__icontains=search_name) | Q(created_by__first_name__icontains=search_name) | Q(market_type__name__icontains=search_name) | Q(id__icontains=search_name)) & Q(is_deleted=False)
        )

    if is_deleted:
        query_filters.append(Q(is_deleted=is_deleted))

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

    

        

