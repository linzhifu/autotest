from django.contrib import admin
from .models import LoginRecord, TestRecord


# Register your models here.
@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = [
        'login_num',
        'login_time',
    ]


@admin.register(TestRecord)
class TestRecordAdmin(admin.ModelAdmin):
    list_display = [
        'test_all',
        'test_pass',
        'test_fail',
        'content_object',
    ]
