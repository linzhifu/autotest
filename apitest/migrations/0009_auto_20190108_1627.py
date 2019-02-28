# Generated by Django 2.1.2 on 2019-01-08 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0008_auto_20190104_0957'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apiinfo',
            options={'ordering': ['-create_time']},
        ),
        migrations.AlterField(
            model_name='apitest',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='测试负责人'),
        ),
    ]