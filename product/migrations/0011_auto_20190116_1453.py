# Generated by Django 2.1.2 on 2019-01-16 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20190115_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-create_time'], 'verbose_name': '产品管理', 'verbose_name_plural': '产品管理'},
        ),
        migrations.RemoveField(
            model_name='product',
            name='level',
        ),
    ]
