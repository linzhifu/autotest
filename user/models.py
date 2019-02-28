from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class LoginRecord(models.Model):
    login_num = models.IntegerField(default=0)
    login_time = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = '登陆计数'
        verbose_name_plural = '登陆计数'
        ordering = [
            '-login_time',
        ]


class TestRecord(models.Model):
    test_all = models.IntegerField(default=0)
    test_pass = models.IntegerField(default=0)
    test_fail = models.IntegerField(default=0)
    test_time = models.DateField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '测试计数'
        verbose_name_plural = '测试计数'
        ordering = [
            '-test_time',
        ]
