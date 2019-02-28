from django.shortcuts import render
from sets.models import Set
from django.contrib.auth.models import User


# Create your views here.
def sets_manage(request):
    user = request.session.get('user', '')
    set_list = Set.objects.all()
    return render(request, 'sets_manage.html', {
        'user': user,
        'sets': set_list
    })


def set_user(request):
    user = request.session.get('user', '')
    user_list = User.objects.all()
    return render(request, 'set_user.html', {
        'user': user,
        'users': user_list
    })
