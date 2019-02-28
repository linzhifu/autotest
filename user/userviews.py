from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import LoginRecord
from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.core.cache import cache
from django.core.mail import EmailMessage
import datetime
import string
import random

# Create your views here.


# 欢迎界面（提示功能未完成）
def welcome(request):
    return render(request, 'welcome.html')


# 用户登陆
def login(request):
    if request.POST:
        username_email = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 判断登陆方式
        # 密码登陆
        if password:
            # 判断邮箱是否存在,存在：获取用户名；不存在：把username_email当用户名
            if User.objects.filter(email=username_email).exists():
                username = User.objects.get(email=username_email).username
            else:
                username = username_email
            # 验证用户密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # 用户密码正确，登陆
                auth.login(request, user)
                request.session['user'] = username
                # 添加一次流量记录，并加入cookie记录，防止刷记录
                if not request.COOKIES.get(username):
                    date = timezone.now().date()
                    login_record, _ = LoginRecord.objects.get_or_create(
                        login_time=date)
                    login_record.login_num += 1
                    login_record.save()
                # home.html 首页
                response = HttpResponseRedirect('/user/home/')
                response.set_cookie(username, 'true', max_age=600)
                return response
            else:
                return render(request, 'login.html', {'error': '用户名或密码错误'})
        # 邮箱动态验证码登陆
        else:
            # 判断邮箱是否存在
            if User.objects.filter(email=username_email).exists():
                code = request.POST.get('code', '')
                # 验证码一致，登陆
                key = username_email.split('@')[0] + email.split('@')[1]
                if request.COOKIES.get(key, '') == code:
                    return render(request, 'login.html',
                                  {'error': '验证码一致,但是功能未完成'})
                else:
                    return render(request, 'login.html', {'error': '验证码错误'})
            # 邮箱不存在
            else:
                return render(request, 'login.html', {'error': '邮箱不存在'})

    else:
        return render(request, 'login.html')


# 首页
@login_required
def home(request):
    # 统计最近七天的访问人数
    date = timezone.now().date()
    login_num = []
    login_times = []
    for i in range(6, -1, -1):
        login_time = date - datetime.timedelta(days=i)
        login_record, _ = LoginRecord.objects.get_or_create(
            login_time=login_time)
        login_num.append(login_record.login_num)
        login_times.append(login_time.strftime('%m/%d'))

    context = {}
    context['login_num'] = login_num
    context['login_times'] = login_times
    response = render(request, 'home.html', context)
    # response.set_cookie('test_apis', 'true', max_age=600)
    return response


# 退出
def logout(request):
    # 用户注销
    auth.logout(request)
    response = HttpResponseRedirect('/user/login/')
    return response


# 获取验证码
def get_code(request):
    data = {}
    # 验证邮箱
    email = request.GET.get('email', '')
    key = email.split('@')[0] + email.split('@')[1]
    # 判断验证码是否已经存在session中
    # if request.session.get(email, ''):
    #     data['status'] = '验证码已发送，请稍后再获取'
    # 判断验证码是否已经存在cookie中
    if request.COOKIES.get(key, ''):
        data['status'] = '验证码已发送，请稍后再获取'
        json = JsonResponse(data)

    else:
        # 获取4位随机数（小写字母+数字）
        code = ''.join(
            random.sample(string.ascii_lowercase + string.digits, 4))
        try:
            # 发送邮件
            # send_mail(
            #     'LONGSYS自动化测试平台',
            #     '验证码：' + code,
            #     '18129832245@163.com',
            #     [email],
            #     fail_silently=False,
            # )
            html_content = "<p><strong>验证码：%s</strong></p>\
                <p>This is an <font size=3 color='green'><strong>important</strong></font> message.</p>" % (
                code)
            msg = EmailMessage(
                'LONGSYS自动化测试平台',
                html_content,
                '18129832245@163.com',
                [email],
            )
            msg.content_subtype = 'html'
            msg.send()
            data['status'] = 'SUCCESS'
            json = JsonResponse(data)
            json.set_cookie(key, code, max_age=300)
            # request.session[email] = code
        except Exception as e:
            print(e)
            data['status'] = '发送失败'
            json = JsonResponse(data)

    return json


# 注册
def register(request):
    if request.POST:
        try:
            # 验证用户名
            username = request.POST.get('username', '').strip()
            if User.objects.filter(username=username).exists():
                raise Exception('用户名已存在')

            # 验证邮箱
            email = request.POST.get('email', '')
            if User.objects.filter(email=email).exists():
                raise Exception('邮箱已存在')

            # 验证验证码
            code = request.POST.get('code', '').lower()
            key = email.split('@')[0] + email.split('@')[1]
            if request.COOKIES.get(key, '') != code:
                raise Exception('验证码错误')

            # 验证输入密码
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            if password != password_again:
                raise Exception('两次输入密码不一致')

            # 注册新用户
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
        except Exception as e:
            return render(request, 'register.html', {'error': e})

        # 注册成功，跳转到首页
        return HttpResponseRedirect('/user/home/')
    else:
        return render(request, 'register.html')


# 重置密码
def change_psw(request):
    if request.POST:
        try:
            # 通过邮箱获取用户
            email = request.POST.get('email', '')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

            else:
                raise Exception('用户不存在')

            # 验证验证码
            code = request.POST.get('code', '').lower()
            key = email.split('@')[0] + email.split('@')[1]
            if request.COOKIES.get(key, '') != code:
                raise Exception('验证码错误')

            # 验证输入密码
            password = request.POST.get('password', '')
            password_again = request.POST.get('password_again', '')
            if password != password_again:
                raise Exception('两次输入密码不一致')

            else:
                user.set_password(password)
                user.save()

        except Exception as e:
            return render(request, 'change_pwd.html', {'error': e})

        # 注册成功，跳转到登陆页面
        return HttpResponseRedirect('/user/login/')

    else:
        return render(request, 'change_pwd.html')
