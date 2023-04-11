from django.urls import path

from .views import index, query_view

app_name = 'warehouses'

urlpatterns = [
    path('', index, name='index'),
    path('query/<int:query_index>/', query_view, name='query_view'),
]
