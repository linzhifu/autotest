# Generated by Django 2.1.2 on 2019-01-08 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20190102_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='creater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='创建人'),
        ),
    ]