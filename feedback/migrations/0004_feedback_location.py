# Generated by Django 3.2.7 on 2021-09-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_multichoiceoption_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='location',
            field=models.CharField(default='', max_length=200, verbose_name='Location'),
        ),
    ]