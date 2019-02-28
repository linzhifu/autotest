from django.urls import path
from apptest import appviews

urlpatterns = [
    path('appcase_manage/', appviews.appcase_manage, name='appcase_manage'),
    path('appcasestep_manage/', appviews.appcasesetp_manage, name='appcasestep_manage'),
    path('appcasesearch/', appviews.appcasesearch, name='appcasesearch'),
    path('appstepsearch/', appviews.appstepsearch, name='appstepsearch'),
]
