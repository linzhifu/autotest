from django.shortcuts import render
from apptest.models import Appcase, Appcasestep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


# Create your views here.
# 流程接口测试
@login_required
def appcase_manage(request):
    appcase_list = Appcase.objects.all()
    appcase_count = appcase_list.count()  # 统计产品数
    username = request.session.get('user', '')  # 读取浏览器登录session
    paginator = Paginator(appcase_list, 8)  # 生成paginator对象,设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        appcase_list = paginator.page(page)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        appcase_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        appcase_list = paginator.page(
            paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容
    return render(request, "appcase_manage.html", {
        "user": username,
        "appcases": appcase_list,
        "currentPage": currentPage,
        "appcasecounts": appcase_count
    })  # 把值赋给apitestcounts这个变量


# 流程接口测试步骤
@login_required
def appcasesetp_manage(request):
    user = request.session.get('user', '')
    appcasesetp_list = Appcasestep.objects.all()
    appcaseid = request.GET.get('appcase.id', None)
    appcase = Appcase.objects.get(id=appcaseid)
    return render(request, 'appcasestep_manage.html', {
        'user': user,
        'appcase': appcase,
        'appcasesteps': appcasesetp_list
    })


# 搜索功能-流程接口测试
@login_required
def appcasesearch(request):
    username = request.session.get('user', '')
    search_appcasename = request.GET.get('appcasename', '')
    appcase_list = Appcase.objects.filter(
        appcasename__icontains=search_appcasename)
    return render(request, 'appcase_manage.html', {
        'user': username,
        'appcases': appcase_list,
    })


# 搜索功能-流程接口测试步骤
@login_required
def appstepsearch(request):
    username = request.session.get('user', '')
    search_appteststep = request.GET.get('appteststep', '')
    appcasesetp_list = Appcasestep.objects.filter(
        appteststep__icontains=search_appteststep)
    return render(request, 'appcasestep_manage.html', {
        'user': username,
        'appcasesteps': appcasesetp_list,
    })