from django.shortcuts import render
from product.models import Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProductForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
# from django.forms.models import model_to_dict


# Create your views here.
# 产品列表
@login_required
def product_manage(request):
    username = request.session.get('user', '')
    user_ojs = User.objects.all()
    search_productname = request.GET.get('productname', '')
    search_productdesc = request.GET.get('productdesc', '')
    search_producter = request.GET.get('producter', '')
    # 按产品名搜索
    if search_productname:
        product_list = Product.objects.filter(
            productname__icontains=search_productname)

    # 按产品描述搜索
    elif search_productdesc:
        product_list = Product.objects.filter(
            productdesc__icontains=search_productdesc)

    # 按产品负责人搜索
    elif search_producter:
        if User.objects.filter(username=search_producter).exists():
            user = User.objects.get(username=search_producter)
            product_list = Product.objects.filter(producter=user)
        else:
            product_list = []

    # 显示全部
    else:
        product_list = Product.objects.all()

    # 生成paginator对象,设置每页显示5条记录
    paginator = Paginator(product_list, 8)
    # 获取当前的页码数,默认为第1页
    page = request.GET.get('page', 1)
    # 把获取的当前页码数转换成整数类型
    currentPage = int(page)
    try:
        # 获取当前页码数的记录列表
        product_list = paginator.page(currentPage)
    except PageNotAnInteger:
        # 如果输入的页数不是整数则显示第1页的内容
        product_list = paginator.page(1)
    except EmptyPage:
        # 如果输入的页数不在系统的页数中则显示最后一页的内容
        product_list = paginator.page(paginator.num_pages)

    # 获取当前页面前后两页的页码
    page_nums = paginator.num_pages  # 总页数
    page_num = product_list.number  # 当前页
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

    product_form = ProductForm()
    context = {}
    context['user'] = username
    context['user_ojs'] = user_ojs
    context['products'] = product_list
    context['page_range'] = page_range
    context['product_form'] = product_form
    return render(request, "product_manage.html", context)


# 搜索功能
@login_required
def search(request):
    # 查询类型
    search_type = request.POST.get('search_type', '').strip()
    # 查询内容
    search_info = request.POST.get('search_info', '').strip()

    return HttpResponseRedirect(
        '/product/list?%s=%s' % (search_type, search_info))


# 新增产品
@login_required
def add(request):
    data = {}
    if request.POST:
        product_form = ProductForm(request.POST)
        # 必须先判断is_valid()，否则cleaned_data不存在
        if product_form.is_valid():
            productname = product_form.cleaned_data['productname']
            if Product.objects.filter(productname=productname).exists():
                # 产品名已存在
                data['status'] = 'ERROR'
            else:
                product_form.cleaned_data['creater'] = request.user
                product_form.save()
                data['status'] = 'SUCCESS'

        else:
            # 产品名已存在
            data['status'] = 'ERROR'

        return JsonResponse(data)
    else:
        pass


# 修改产品
@login_required
def modify(request):
    data = {}
    pk = request.GET.get('pk', '')
    # 获取对比对象
    product = Product.objects.get(pk=pk)
    # 模型转为字典，后续比较数据
    # data = model_to_dict(product)
    # 注意 instance=product因为是用ProductForm修改 部分字段，这时候需要指定修改的是哪个实例，否则是新建
    # product_form = ProductForm(request.POST, initial=data, instance=product)
    product_form = ProductForm(request.POST, instance=product)
    # 因为表单中含有csrf_token数据，所以肯定会有数据变化
    if product_form.has_changed:
        if len(product_form.changed_data):
            for field in product_form.changed_data:
                print(field + '已被修改')
                if field == 'productname':
                    productname = request.POST.get('productname', '')
                    if Product.objects.filter(
                            productname=productname).exists():
                        data['status'] = 'ERROR'
                        data['info'] = '产品名已存在'
                        return JsonResponse(data)
                        # return HttpResponseRedirect('/product/list/')

            if product_form.is_valid():
                product_form.save()
                data['status'] = 'SUCCESS'
                return JsonResponse(data)
        else:
            data['status'] = 'ERROR'
            data['info'] = '没有变化，请修改后保存'
            return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['info'] = '没有变化，请修改后保存'
        return JsonResponse(data)

    # return HttpResponseRedirect('/product/list/')


# 删除产品
@login_required
def delete(request):
    data = {}
    # 判断是否是超级管理员
    if request.user == User.objects.all()[0]:
        pk = request.GET.get('pk', '')
        product = Product.objects.get(pk=pk)
        data['status'] = 'SUCCESS'
        product.delete()
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
