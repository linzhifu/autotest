# Generated by Django 2.1.2 on 2019-01-17 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0021_apiinfo_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apiinfo',
            options={'ordering': ['-level']},
        ),
    ]
