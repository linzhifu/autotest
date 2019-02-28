from django import forms
from .models import Apis, Apiinfo


class ApisForm(forms.ModelForm):
    class Meta:
        model = Apis
        fields = (
            'Product',
            'apiname',
            'apiurl',
            'apitester',
        )

        widgets = {
            'Product':
            forms.widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': '请输入产品名称',
            }),
            'apiname':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入API模块'
            }),
            'apiurl':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入URL'
            }),
            'apitester':
            forms.widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': '请选择负责人'
            }),
        }

    # def clean_apiname(self):
    #     # 检查API是否已存在
    #     apiname = self.cleaned_data['apiname']
    #     if Apis.objects.filter(apiname=apiname).exists():
    #         raise forms.ValidationError('API已存在')
    #     return apiname


class ApiinfoForm(forms.ModelForm):
    class Meta:
        model = Apiinfo
        fields = {
            'api',
            'apiname',
            'bodytype',
            'apimethod',
            'apiurl',
            'apiparamvalue',
            'apijson',
            'apiresponse',
            'level',
        }

#     def clean_apiname(self):
#         # 检查API是否已存在
#         apiname = self.cleaned_data['apiname']
#         if Apiinfo.objects.filter(apiname=apiname).exists():
#             raise forms.ValidationError('APIINFO已存在')
#         return apiname

#     def clean_bodytype(self):
#         # 检查API是否已存在
#         bodytype = self.cleaned_data['bodytype']
#         return bodytype

#     def clean_apimethod(self):
#         # 检查API是否已存在
#         apimethod = self.cleaned_data['apimethod']
#         return apimethod

#     def clean_apiurl(self):
#         # 检查API是否已存在
#         apiurl = self.cleaned_data['apiurl']
#         return apiurl

#     def clean_apiparamvalue(self):
#         # 检查API是否已存在
#         apiparamvalue = self.cleaned_data['apiparamvalue']
#         return apiparamvalue

#     def clean_apijson(self):
#         # 检查API是否已存在
#         apijson = self.cleaned_data['apijson']
#         return apijson

#     def clean_apiresponse(self):
#         # 检查API是否已存在
#         apiresponse = self.cleaned_data['apiresponse']
#         return apiresponse
