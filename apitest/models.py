from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Apis(models.Model):
    Product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, null=True)  # 关联产品id
    apiname = models.CharField('后端模块', max_length=100, help_text='请输入后端模块')  # 接口标题，help_text：admin模式下帮助文档
    apiurl = models.CharField('url地址', max_length=200)  # 地址
    # apitester = models.CharField('测试负责人', max_length=16, null=True)  # 执行人
    apitester = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='测试负责人')  # 关联用户
    level = models.IntegerField('测试基本', default=-1)
    apistatus = models.BooleanField('是否通过', default=True)  # 测试结果
    create_time = models.DateTimeField(
        '创建时间', auto_now_add=True)  # 创建时间-自动获取当前时间
    update_time = models.DateTimeField('修改时间', auto_now=True)  # 创建时间-自动获取当前时间

    class Meta:
        verbose_name = 'API测试用例'
        verbose_name_plural = 'API测试用例'
        ordering = [
            '-create_time',
        ]

    def __str__(self):
        return self.apiname


class Apiinfo(models.Model):
    api = models.ForeignKey(
        'Apis',
        on_delete=models.CASCADE,
        null=True,
    )
    # 接口标题
    apiname = models.CharField('接口名称', max_length=100)
    # body类型
    BODY_TYPE = (
        ('application/json;charset=utf-8', 'application/json;charset=utf-8'),
        ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'))
    bodytype = models.CharField(
        verbose_name='body类型',
        choices=BODY_TYPE,
        default='json',
        max_length=200)
    # 请求方法
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'),
                      ('delete', 'delete'), ('patch', 'patch'))
    apimethod = models.CharField(
        verbose_name='请求方法',
        choices=REQUEST_METHOD,
        default='get',
        max_length=200)
    # 地址
    apiurl = models.CharField('url地址', max_length=200)
    # 请求参数和值param
    apiparamvalue = models.TextField(
        '请求参数param', max_length=800, null=True, blank=True)
    # 请求数据JSON
    apijson = models.TextField(
        '请求数据json', max_length=800, null=True, blank=True)
    # 响应数据
    apiresponse = models.TextField(
        '响应数据json',
        max_length=5000
    )
    level = models.IntegerField('测试基本', default=-1)
    # 测试结果
    apistatus = models.BooleanField('是否通过', default=True)
    # 创建时间-自动获取当前时间
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        ordering = [
            '-level',
        ]

    def __str__(self):
        return self.apiname
