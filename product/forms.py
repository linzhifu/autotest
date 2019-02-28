from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'productname',
            'productdesc',
            'producter',
            # 'level',
        )
        widgets = {
            'productname':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入产品名称',
            }),
            'productdesc':
            forms.widgets.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入产品描述'
            }),
            'producter':
            forms.widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': '请输入产品负责人'
            }),
            # 'level':
            # forms.widgets.NumberInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': '请输入产品级别,用于排序'
            # }),
        }

    # def clean_productname(self):
    #     # 检查产品名是否已存在
    #     productname = self.cleaned_data['productname']
    #     if Product.objects.filter(productname=productname).exists():
    #         raise forms.ValidationError('产品名已存在')
    #     return productname
