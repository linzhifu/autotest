from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    productname = models.CharField('产品名称', max_length=64)  # 产品名称
    productdesc = models.CharField('产品描述', max_length=200)  # 产品描述
    producter = models.ForeignKey(
        User,
        related_name='producter',
        on_delete=models.CASCADE,
        verbose_name='负责人')
    creater = models.ForeignKey(
        User,
        related_name='creater',
        on_delete=models.CASCADE,
        verbose_name='创建人',
        default=1)
    # level = models.IntegerField('产品级别', default=-1)
    create_time = models.DateTimeField('创建时间', auto_now=True)  # 创建时间-自动获取当前时间

    class Meta:
        verbose_name = '产品管理'
        verbose_name_plural = '产品管理'
        ordering = [
            '-create_time',
        ]

    def __str__(self):
        return self.productname
