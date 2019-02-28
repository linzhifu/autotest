from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Webcase(models.Model):

    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE)  # 关联产品id
    webcasename = models.CharField('用例名称', max_length=200)  # 测试用例名称
    apiurl = models.CharField('url地址', max_length=200)  # 地址
    webtestresult = models.BooleanField('测试结果')  # 测试结果
    webtester = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='测试负责人')  # 关联用户
    create_time = models.DateTimeField(
        '创建时间', auto_now_add=True)  # 创建时间-自动获取当前时间
    update_time = models.DateTimeField('修改时间', auto_now=True)  # 修改时间-自动获取当前时间

    class Meta:
        verbose_name = 'web测试用例'
        verbose_name_plural = 'web测试用例'

    def __str__(self):
        return self.webcasename


class Webcasestep(models.Model):

    webcase = models.ForeignKey(Webcase, on_delete=models.CASCADE)  # 关联接口id
    webtestobjname = models.CharField('测试对象名称描述', max_length=200)  # 测试对象名称描述
    webevelement = models.CharField('CSS选择器', max_length=800)  # 控件元素
    weboptmethod = models.CharField('操作方法', max_length=200)  # 操作方法
    webtestresult = models.BooleanField('测试结果')  # 测试结果
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    def __str__(self):
        return self.webtestobjname
