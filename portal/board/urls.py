from django.urls import path
from .views import AdList, AdDetail, AdCreate

urlpatterns = [
    path('', AdList.as_view(), name='ad_list_view'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail_view'),
    path('create', AdCreate.as_view(), name='ad_create_view'),
]
