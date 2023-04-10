from django.contrib import admin
from django.urls import path

from .views import (index, query_1, query_2, query_3, query_4, query_5,
                    query_6, query_7, query_8, query_9, query_10)

app_name = 'warehouses'

urlpatterns = [
    path('query-1/', query_1, name='query_1'),
    path('query-2/', query_2, name='query_2'),
    path('query-3/', query_3, name='query_3'),
    path('query-4/', query_4, name='query_4'),
    path('query-5/', query_5, name='query_5'),
    path('query-6/', query_6, name='query_6'),
    path('query-7/', query_7, name='query_7'),
    path('query-8/', query_8, name='query_8'),
    path('query-9/', query_9, name='query_9'),
    path('query-10/', query_10, name='query_10'),
]
