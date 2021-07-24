from django.urls import path
from .views import AdFiltered, AdList, AdDetail, AdCreate, AdEdit, AdDelete,\
    ReplyCreate, ReplyDelete

urlpatterns = [
    path('', AdList.as_view(), name='ad_list_view'),
    path('<int:pk>', AdDetail.as_view(), name='ad_detail_view'),
    path('ad/create', AdCreate.as_view(), name='ad_create_view'),
    path('ad/<int:pk>/edit', AdEdit.as_view(), name='ad_edit_view'),
    path('ad/<int:pk>/delete', AdDelete.as_view(), name='ad_delete_view'),
    path('ad/filtered', AdFiltered.as_view(), name='ad_filtered_view'),
    path('reply/<int:ad_id>/create', ReplyCreate.as_view(),
         name='reply_create_view'),
    path('reply/<int:pk>/delete', ReplyDelete.as_view(),
         name='reply_delete_view'),
]
