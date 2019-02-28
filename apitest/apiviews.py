from django.shortcuts import render
from apitest.models import Apis, Apiinfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from apitest.tests import get_record, login
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ApisForm, ApiinfoForm
from django.contrib.auth.models import User
# from django.forms.models import model_to_dict
from product.models import Product
from .tests import test_apis

# Create your views here.


# test
def test(request):
    test_apis()
    return JsonResponse({})


# 获取测试登陆信息
def test_login(request):
    data = {}
    data['info'] = login()
    return JsonResponse(data)


# API测试用例
@login_required
def apis_manage(request):
    product_id = request.GET.get('product_id', '')
    apiname = request.GET.get('apiname', '')
    productname = request.GET.get('productname', '')
    if product_id:
        apis_list = Apis.objects.filter(Product_id=product_id)
    elif apiname:
        apis_list = Apis.objects.filter(apiname__icontains=apiname)
    elif productname:
        apis_list = Apis.objects.filter(
            Product__productname__icontains=productname)
    else:
        apis_list = Apis.objects.all()
        print('all')
    username = request.session.get('user', '')
    paginator = Paginator(apis_list, 8)  # 生成paginator对象,设置每页显示8条记录
    page = request.GET.get('page', 1)  # 获取当前的页码数,默认为第1页
    currentPage = int(page)  # 把获取的当前页码数转换成整数类型
    try:
        apis_list = paginator.page(currentPage)  # 获取当前页码数的记录列表
    except PageNotAnInteger:
        apis_list = paginator.page(1)  # 如果输入的页数不是整数则显示第1页的内容
    except EmptyPage:
        apis_list = paginator.page(
            paginator.num_pages)  # 如果输入的页数不在系统的页数中则显示最后一页的内容

    # 获取当前页面前后两页的页码
    page_nums = paginator.num_pages  # 总页数
    page_num = apis_list.number  # 当前页
    page_range = [
        x for x in range(int(page_num) - 2,
                         int(page_num) + 3) if 0 < x <= page_nums
    ]
    # 给页码加首页和尾页，间隔页加'...'
    if page_range[0] - 1 > 1:
        page_range.insert(0, '...')
    if page_range[-1] + 1 < page_nums:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != page_nums:
        page_range.append(page_nums)
    apis_form = ApisForm()
    context = {}
    context['product_id'] = product_id
    context['product_ojs'] = Product.objects.all()
    context['user'] = username
    context['user_ojs'] = User.objects.all()
    context['apiss'] = apis_list
    context['page_range'] = page_range
    context['apis_form'] = apis_form
    return render(request, "apis_manage.html", context)  # 把值赋给apiscounts这个变量


# 搜索功能
@login_required
def apissearch(request):
    search_info = request.GET.get('search_info', '').strip()
    search_type = request.GET.get('search_type', '').strip()
    return HttpResponseRedirect(
        '/apitest/apis_manage/?%s=%s' % (search_type, search_info))


# 修改API
@login_required
def modify_apis(request):
    data = {}
    pk = request.GET.get('pk', '')
    product_id = request.GET.get('product_id', '')
    # 获取对比对象
    apis = Apis.objects.get(pk=pk)
    # 模型转为字典，后续比较数据
    # data = model_to_dict(apis)
    # 注意 instance=apis因为是用ApisForm修改 部分字段，这时候需要指定修改的是哪个实例，否则是新建
    # apis_form = ApisForm(request.POST, initial=data, instance=apis)
    apis_form = ApisForm(request.POST, instance=apis)
    # 因为表单中含有csrf_token数据，所以肯定会有数据变化
    if apis_form.has_changed:
        if len(apis_form.changed_data):
            for field in apis_form.changed_data:
                print(field + '已被修改')
                # 判断修改后名称是否存在
                if field == 'apiname':
                    apiname = request.POST.get('apiname', '')
                    if Apis.objects.filter(
                            apiname=apiname, Product_id=product_id).exists():
                        data['status'] = 'ERROR'
                        data['info'] = 'API名称已存在'
                        return JsonResponse(data)
                        # return HttpResponseRedirect(
                        #     '/apitest/apis_manage/?product_id=%s' %
                        #     (product_id))

            if apis_form.is_valid():
                apis_form.save()
                data['status'] = 'SUCCESS'
                return JsonResponse(data)
        else:
            data['status'] = 'ERROR'
            data['info'] = '数据没有变化'
            return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['info'] = '数据没有变化'
        return JsonResponse(data)

    # return HttpResponseRedirect(
    #     '/apitest/apis_manage/?product_id=%s' % (product_id))


# 添加API模块
@login_required
def add(request):
    data = {}
    if request.POST:
        apis_form = ApisForm(request.POST)
        # 必须先判断is_valid()，否则cleaned_data不存在
        if apis_form.is_valid():
            apiname = apis_form.cleaned_data['apiname']
            product_id = apis_form.cleaned_data['Product']
            if Apis.objects.filter(
                    apiname=apiname, Product_id=product_id).exists():
                # API已存在
                data['status'] = 'ERROR'
            else:
                apis_form.cleaned_data['creater'] = request.user
                apis_form.save()
                data['status'] = 'SUCCESS'

        else:
            # API已存在
            data['status'] = 'ERROR'
        return JsonResponse(data)
    else:
        pass


# 删除API模块
@login_required
def delete(request):
    data = {}
    # 判断是不是超级管理员
    if request.user == User.objects.all()[0]:
        pk = request.GET.get('pk', '')
        apis = Apis.objects.filter(pk=pk)
        apis.delete()
        data['status'] = 'SUCCESS'

    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


# API具体内容
@login_required
def apiinfos_manage(request):
    # 获取登陆API信息，用于后续测试
    # response = login()

    user = request.session.get('user', '')
    apisid = request.GET.get('apis.id', None)
    apis = Apis.objects.get(id=apisid)
    apiinfos_list = Apiinfo.objects.filter(api_id=apisid)
    # 获取测试记录
    test_times, test_all, test_pass, test_fail = get_record(apis)
    context = {}
    context['user'] = user
    context['apis'] = apis
    context['apiinfos'] = apiinfos_list
    context['test_times'] = test_times
    context['test_all'] = test_all
    context['test_pass'] = test_pass
    context['test_fail'] = test_fail
    # context['response'] = response
    context['apiinfo_form'] = ApiinfoForm()
    return render(request, 'apiinfos_manage.html', context)


# 添加API内容信息
@login_required
def add_apiinfo(request):
    # json对象字典
    data = {}
    if request.POST:
        apiinfo_form = ApiinfoForm(request.POST)
        apis_id = request.POST.get('api')
        apiname = request.POST.get('apiname')
        if Apiinfo.objects.filter(apiname=apiname, api_id=apis_id).exists():
            data['status'] = 'ERROR'
        else:
            if apiinfo_form.is_valid():
                apiinfo_form.save()
                data['status'] = 'SUCCESS'

            else:
                print(apiinfo_form.errors)
                data['status'] = 'ERROR'

        return JsonResponse(data)


# 删除API内容信息
@login_required
def delete_info(request):
    data = {}
    if request.user == User.objects.all()[0]:
        pk = request.GET.get('pk', '')
        apiinfo = Apiinfo.objects.get(pk=pk)
        data['status'] = 'SUCCESS'
        apiinfo.delete()
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


# 修改API内容信息
@login_required
def modify_apiinfo(request):
    data = {}
    pk = request.GET.get('pk')
    apis_id = request.GET.get('apis_id')
    apiinfo = Apiinfo.objects.get(pk=pk)
    # data = model_to_dict(apiinfo)
    # data.pop('id')
    # data.pop('apistatus')
    # 注意 instance=apiinfo因为是用ModelForm修改 部分字段，这时候需要指定修改的是哪个实例，否则是新建
    # apiinfo_form = ApiinfoForm(request.POST, initial=data, instance=apiinfo)
    apiinfo_form = ApiinfoForm(request.POST, instance=apiinfo)
    # 因为表单中含有csrf_token数据，所以肯定会有数据变化
    if apiinfo_form.has_changed:
        if len(apiinfo_form.changed_data):
            for field in apiinfo_form.changed_data:
                print(field + '已被修改')
                # 判断修改后名称是否存在
                if field == 'apiname':
                    apiname = request.POST.get('apiname', '')
                    if Apiinfo.objects.filter(
                            apiname=apiname, api_id=apis_id).exists():
                        data['status'] = 'ERROR'
                        data['info'] = 'API接口名称已存在'
                        return JsonResponse(data)
                        # return HttpResponseRedirect(
                        #     '/apitest/apiinfos_manage/?apis.id=%s' % (apis_id))

            if apiinfo_form.is_valid():
                apiinfo_form.cleaned_data['api'] = Apis.objects.get(pk=apis_id)
                print(apiinfo_form.cleaned_data['api'])
                apiinfo_form.save()
                # 修改成功
                data['status'] = 'SUCCESS'
                return JsonResponse(data)
        else:
            data['status'] = 'ERROR'
            data['info'] = '数据没有变化'
            return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['info'] = '数据没有变化'
        return JsonResponse(data)
    # return HttpResponseRedirect(
    #     '/apitest/apiinfos_manage/?apis.id=%s' % (apis_id))
