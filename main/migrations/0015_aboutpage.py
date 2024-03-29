# Generated by Django 3.2.7 on 2021-09-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210126_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('current', models.BooleanField(default=True, verbose_name='Current')),
            ],
            options={
                'verbose_name': 'About Page',
            },
        ),
    ]
