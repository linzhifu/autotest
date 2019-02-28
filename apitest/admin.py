from django.contrib import admin
from apitest.models import Apis, Apiinfo

# Register your models here.


class ApiinfosAdmin(admin.TabularInline):
    model = Apiinfo
    # fieldsets = (
    #     ('API描述', {'fields': ('apiname',)}),
    #     ('API参数', {'fields': ('apimethod', 'apiparamvalue', 'apijson')}),
    #     ('API响应', {'fields': ('apiresponse',)})
    #     )
    extra = 1


@admin.register(Apis)
class ApisAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'Product', 'apiname', 'apiurl', 'apitester', 'apistatus',
        'create_time', 'update_time'
    ]
    inlines = [ApiinfosAdmin]


# admin.site.register(Apis, ApisAdmin)
admin.site.site_title = 'LONGSYS'
admin.site.site_header = '自动化测试平台'
