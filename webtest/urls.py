from django.urls import path
from webtest import webviews

urlpatterns = [
    path('webcase_manage/', webviews.webcase_manage, name='webcase_manage'),
    path('webcasestep_manage/', webviews.webcasesetp_manage, name='webcasestep_manage'),
    path('webcasesearch/', webviews.webcasesearch, name='webcasesearch'),
    path('webstepsearch/', webviews.webstepsearch, name='webstepsearch'),
]