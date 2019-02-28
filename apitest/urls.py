from django.urls import path
from apitest import apiviews

urlpatterns = [
    path('apis_manage/', apiviews.apis_manage, name='apis_manage'),
    path('apiinfos_manage/', apiviews.apiinfos_manage, name='apiinfos_manage'),
    path('apissearch/', apiviews.apissearch, name='apissearch'),
    path('add/', apiviews.add, name='addapis'),
    path('delete/', apiviews.delete, name='deleteapis'),
    path('modifyinfo', apiviews.modify_apiinfo, name='modifyapi'),
    path('delete_info/', apiviews.delete_info, name='deleteapiinfo'),
    path('add_apiinf/', apiviews.add_apiinfo, name='addapiinfo'),
    path('modify_apis/', apiviews.modify_apis, name='apis_modify'),
    path('test/', apiviews.test, name='apitest'),
    path('test_login/', apiviews.test_login, name='test_login')
]
