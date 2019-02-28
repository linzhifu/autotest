from django.urls import path
from product import proviews

urlpatterns = [
    path('list/', proviews.product_manage, name='product_manage'),
    path('search/', proviews.search, name='prosearch'),
    path('add/', proviews.add, name='addpro'),
    path('delete/', proviews.delete, name='deletepro'),
    path('modify/', proviews.modify, name='pro_modify')
]
