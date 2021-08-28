from django.urls import path
from .views import AdFiltered, AdList, AdDetail, AdCreate, AdEdit, AdDelete,\
    ReplyCreate, ReplyDelete, ReplyConfirmApprove, ReplyList, approve_reply,\
    NewsList, NewsDetail, NewsCreate, NewsEdit, NewsDelete, news_subscribe,\
    news_unsubscribe, NewsMailingConfirm, news_mailing_confirm,\
    NewsDetailApi, AdListApi, NewsCreateApi, NewsListApi, NewsMailingApi,\
    NewsEditApi, NewsDeleteApi, AdCreateApi, AdDetailApi, AdEditApi,\
    MyAdFilteredApi, AdDeleteApi, MyRepliesApi
from django.views.generic import TemplateView
from rest_framework.authtoken import views


urlpatterns = [
    path('ad', AdList.as_view(), name='ad_list_view'),
    path('ad/<int:pk>', AdDetail.as_view(), name='ad_detail_view'),
    path('ad/create', AdCreate.as_view(), name='ad_create_view'),
    path('ad/<int:pk>/edit', AdEdit.as_view(), name='ad_edit_view'),
    path('ad/<int:pk>/delete', AdDelete.as_view(), name='ad_delete_view'),
    path('ad/filtered', AdFiltered.as_view(), name='ad_filtered_view'),
    path('reply', ReplyList.as_view(), name='reply_list_view'),
    path('reply/<int:ad_id>/create', ReplyCreate.as_view(),
         name='reply_create_view'),
    path('reply/<int:pk>/delete', ReplyDelete.as_view(),
         name='reply_delete_view'),
    path('reply/<int:pk>/approve', ReplyConfirmApprove.as_view(),
         name='reply_approve_view'),
    path('reply/<int:pk>/approve_confirm', approve_reply,
         name='reply_approve_button'),
    path('news', NewsList.as_view(), name='news_list_view'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail_view'),
    path('news/create', NewsCreate.as_view(), name='news_create_view'),
    path('news/<int:pk>/edit', NewsEdit.as_view(), name='news_edit_view'),
    path('news/<int:pk>/delete', NewsDelete.as_view(),
         name='news_delete_view'),
    path('news/subscribe', news_subscribe, name='news_subscribe_button'),
    path('news/unsubscribe', news_unsubscribe, name='news_unsubscribe_button'),
    path('news/<int:pk>/mailing', NewsMailingConfirm.as_view(),
         name='news_confirm_mailing_view'),
    path('news/<int:pk>/mailing_confirm', news_mailing_confirm,
         name='news_confirm_mailing_button'),
    path('swagger-ui/', TemplateView.as_view(
         template_name='swagger/index.html',
         extra_context={'schema_url': 'openapi-schema.yml'},),
         name='swagger-ui'),
    path('api/token_auth', views.obtain_auth_token,
         name='obtain_auth_token_api'),
    path('api/news/', NewsListApi.as_view(), name='news_list_api'),
    path('api/news/<int:pk>/', NewsDetailApi.as_view(),
         name='news_detail_api'),
    path('api/news/<int:pk>/mailing', NewsMailingApi.as_view(),
         name='news_mailing_api'),
    path('api/news/create/', NewsCreateApi.as_view(),
         name='news_create_api'),
    path('api/news/<int:pk>/edit', NewsEditApi.as_view(),
         name='news_edit_api'),
    path('api/news/<int:pk>/delete', NewsDeleteApi.as_view(),
         name='news_delete_api'),
    path('api/ad/', AdListApi.as_view(), name='ad_list_api'),
    path('api/ad/filtered', MyAdFilteredApi.as_view(), name='ad_filtered_api'),
    path('api/ad/<int:pk>/', AdDetailApi.as_view(),
         name='ad_detail_api'),
    path('api/ad/create/', AdCreateApi.as_view(),
         name='ad_create_api'),
    path('api/ad/<int:pk>/edit', AdEditApi.as_view(),
         name='ad_edit_api'),
    path('api/ad/<int:pk>/delete', AdDeleteApi.as_view(),
         name='ad_delete_api'),
    path('api/reply/', MyRepliesApi.as_view(), name='reply_list_api'),
]
