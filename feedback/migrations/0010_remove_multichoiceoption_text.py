# Generated by Django 3.2.7 on 2021-09-27 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0009_auto_20210927_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multichoiceoption',
            name='text',
        ),
    ]