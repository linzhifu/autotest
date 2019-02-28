from django.shortcuts import render
from webtest.models import Webcase, Webcasestep
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


# Create your views here.
# 流程接口测试
@login_required
def webcase_manage(request):
    webcase_list = Webcase.objects.all()
    webcase_count = webcase_list.count()  # 统计产品数
    username = request.session.get('user', '')  # 读取浏览器登录session
    paginator = Paginator(webcase_list, 8)  # 生成paginator对象,设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        webcase_list = paginator.page(page)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        webcase_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        webcase_list = paginator.page(
            paginator.num_pages)  #如果输入的页数不在系统的页数中则显示最后一页
    return render(request, "webcase_manage.html", {
        "user": username,
        "webcases": webcase_list,
        "currentPage": currentPage,
        "webcasecounts": webcase_count
    })


# 流程接口测试步骤
@login_required
def webcasesetp_manage(request):
    username = request.session.get('user', '')

    webcaseid = request.GET.get('webcase.id', None)
    webcase = Webcase.objects.get(id=webcaseid)
    webcasestep_list = Webcasestep.objects.all()
    return render(request, "webcasestep_manage.html", {
        "user": username,
        "webcase": webcase,
        "webcasesteps": webcasestep_list
    })


# 搜索功能-流程接口测试
@login_required
def webcasesearch(request):
    username = request.session.get('user', '')
    search_webcasename = request.GET.get('webcasename', '')
    webcase_list = Webcase.objects.filter(
        webcasename__icontains=search_webcasename)
    return render(request, 'webcase_manage.html', {
        'user': username,
        'webcases': webcase_list
    })


# 搜索功能-流程接口测试步骤
@login_required
def webstepsearch(request):
    username = request.session.get('user', '')
    search_webteststep = request.GET.get('webteststep', '')
    webcasesetp_list = Webcasestep.objects.filter(
        webteststep__icontains=search_webteststep)
    return render(request, 'webcasestep_manage.html', {
        'user': username,
        'webcasesteps': webcasesetp_list,
    })
