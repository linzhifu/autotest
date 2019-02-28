from django.contrib import admin
from product.models import Product
from apitest.models import Apis
from apptest.models import Appcase

# Register your models here.


class ApisAdmin(admin.TabularInline):
    list_display = [
        'apiname', 'apiurl', 'apiparamvalue', 'apimethod', 'apiresult',
        'apistatus', 'create_time', 'id', 'product'
    ]
    model = Apis
    extra = 1


class AppcaseAdmin(admin.TabularInline):
    list_display = ['appcasename', 'apptestresult', 'create_time', 'id']
    model = Appcase
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'productname',
        'productdesc',
        'producter',
        'creater',
        'create_time',
        'id',
    ]
    inlines = [ApisAdmin, AppcaseAdmin]


admin.site.register(Product, ProductAdmin)
