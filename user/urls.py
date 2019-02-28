from django.urls import path
from user import userviews

urlpatterns = [
    path('login/', userviews.login, name='login'),
    path('home/', userviews.home, name='home'),
    path('logout/', userviews.logout, name='logout'),
    path('register/', userviews.register, name='register'),
    path('get_code/', userviews.get_code, name='get_code'),
    path('change_pwd/', userviews.change_psw, name='change_pwd'),
    path('welcome/', userviews.welcome, name='welcome')
]
