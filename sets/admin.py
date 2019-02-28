from django.contrib import admin

# Register your models here.
from sets.models import Set


class SetAdmin(admin.ModelAdmin):
    list_display = ['setname', 'setvalue', 'id']


admin.site.register(Set)
